#include <cmath>

#include "dreal/solver/branch_gradient_descent.h"
#include "dreal/util/eigen.h"
#include "dreal/util/evaluation_visitor.h"

namespace dreal {

using std::pair;
using std::vector;

namespace {

/// Returns the center point of box @p b.
Eigen::VectorXd ExtractCenterPoint(const Box& b) {
  Eigen::VectorXd c{b.size()};
  for (int i{0}; i < b.size(); ++i) {
    if (b[i].lb() == -INFINITY) {
      c[i] = b[i].ub();
    } else if (b[i].ub() == +INFINITY) {
      c[i] = b[i].lb();
    } else {
      c[i] = b[i].mid();
    }
  }
  return c;
}

// Set @p box to the point @p p.
void SetBox(const Eigen::VectorXd& p, Box* const box) {
  for (int i{0}; i < box->size(); ++i) {
    (*box)[i] = p[i];
  }
}

/// Clamps *this by the box b and returns a reference to *this.
void Clamp(const Box& b, double* const p) {
  for (int i{0}; i < b.size(); ++i) {
    double& value{p[i]};
    const Box::Interval& iv{b[i]};
    if (value < iv.lb()) {
      value = iv.lb();
    } else if (iv.ub() < value) {
      value = iv.ub();
    }
  }
}

/// Initialize q with p.
void InitializeAutodiff(const Eigen::VectorXd& p,
                        VectorX<Eigen::AutoDiffScalar<Eigen::VectorXd>>* q) {
  const auto size_of_p{p.size()};
  for (int i{0}; i < size_of_p; ++i) {
    (*q)[i] = p[i];
    (*q)(i).derivatives() = Eigen::VectorXd::Unit(size_of_p, i);
  }
}

bool IncludeNaN(const Eigen::VectorXd& v) { return v.array().isNaN().any(); }

}  // namespace

// P = Sample(box)  # For now, just take the center point.
// α = 0.001        # parameter.
//
// # Goal: Move P to minimize errors
// for i = 1 to MAX_ITER:
//     stop = true
//
//     for f in constraints:
//         error = f(P)
//         if error ≥ 0:
//             P' -= α * ∇f(P) * error
//             error' = f(P')
//             if error' < error:
//                 P = P'
//                 stop = false
//
//     if stop:
//         # It turns out that no constraint can move P.
//         # We stop here.
//         break
bool BranchGradientDescent(const vector<FormulaEvaluator>& formula_evaluators,
                           const Config& config,
                           const ibex::BitSet& branching_candidates, Box* box,
                           vector<pair<Box, int>>* stack) {
  // Constants
  constexpr int kMaxIter{3};
  constexpr double kAlpha{1};

  // 1. Sample a point (an environment), P (maybe take the center)
  Eigen::VectorXd p{ExtractCenterPoint(*box)};

  // 2. Constructs the error functions by turning formulas into
  // expressions.
  VectorX<Expression> constraints(static_cast<int>(formula_evaluators.size()));
  for (size_t i{0}; i < formula_evaluators.size(); ++i) {
    const FormulaEvaluator& formula_evaluator{formula_evaluators[i]};
    constraints[i] = ToErrorFunction(formula_evaluator.formula());
  }
  // 3. Take the Jacobian of the constraints at the current point P, and
  //    move P to P' using the Jacobian.
  //
  // If there is a constraint which moves P to P' and reduce the
  // error, it keep iterating. Otherwise, it stops.
  VectorX<Eigen::AutoDiffScalar<Eigen::VectorXd>> q(p.size());
  const EvaluationVisitor evaluation_visitor{box->variables()};
  bool stop{false};

  // InitializeAutodiff(p, &q);  // Initialize q as p.
  // VectorX<Eigen::AutoDiffScalar<Eigen::VectorXd>> eval{
  //     evaluation_visitor.Evaluate<Eigen::AutoDiffScalar<Eigen::VectorXd>>(
  //         constraints, q)};
  // if ((eval.array() <= config.precision()).all()) {
  //   DREAL_LOG_TRACE("All the errors are smaller than {}: {}",
  //                   config.precision(), eval.value());
  //   SetBox(p, box);
  //   return true;
  // }

  // bool need_to_eval{false};

  for (int i{0}; i < kMaxIter && !stop; ++i) {
    stop = true;
    DREAL_LOG_TRACE("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~");
    for (size_t j{0}; j < formula_evaluators.size(); ++j) {
      const Formula& f_j{formula_evaluators[j].formula()};
      const Expression& e_j{constraints[j]};

      InitializeAutodiff(p, &q);  // Initialize q as p.
      Eigen::AutoDiffScalar<Eigen::VectorXd> eval =
          evaluation_visitor.Evaluate<Eigen::AutoDiffScalar<Eigen::VectorXd>>(
              e_j, q);
      // if ((eval.array() <= config.precision()).all()) {
      //   DREAL_LOG_TRACE("All the errors are smaller than {}: {}",
      //                   config.precision(), eval.value());
      //   SetBox(p, box);
      //   return true;
      // }

      const double current_error{eval.value()};
      DREAL_LOG_TRACE("{}-th iteration, {}-th constraint {}, Error: {}", i, j,
                      f_j, current_error);
      DREAL_LOG_TRACE("Before Change: P = {}", p.transpose());
      if (current_error > 0.0) {
        const auto derivatives{eval.derivatives()};
        DREAL_LOG_TRACE("Derivatives = {}", derivatives.transpose());
        if (IncludeNaN(derivatives)) {
          DREAL_LOG_TRACE("Derivatives include NaN. Skip this.");
          continue;
        }
        const auto delta = derivatives * kAlpha * error;
        DREAL_LOG_TRACE("Delta = {}", delta.transpose());
        const double new_error =
            evaluation_visitor.Evaluate<double>(e_j, (p - delta));
        if (new_error < current_error) {
          DREAL_LOG_ERROR("Improved: Error {} => {}", current_error, new_error);
          stop = false;
          p -= delta;
          Clamp(*box, p.data());
          DREAL_LOG_TRACE("After Change : P = {}", p.transpose());
        }
      } else {
        DREAL_LOG_TRACE("Current Error is negative, do nothing.");
        continue;
      }
    }
  }
  const auto final_error = evaluation_visitor.Evaluate<double>(constraints, p);
  if ((final_error.array() <= config.precision()).all()) {
    std::cerr << "P = " << p << " is a solution!!!!!!!!!!\n";
    SetBox(p, box);
    return true;
  }
  // else {
  // std::cerr << "P is not a solution\n"
  //           << "Error = " << final_error.transpose() << std::endl;
  // for (int i = 0; i < box->size(); ++i) {
  //   std::cerr << box->variable(i) << " : " << p[i] << " in " << (*box)[i]
  //             << "\n";
  // }
  // for (int i = 0; i < constraints.size(); ++i) {
  //   std::cerr << i << "\t" << formula_evaluators[i].formula() << "\n"
  //             << i << "\t" << constraints[i] << std::endl;
  // }
  // }

  double max_shift = -999;
  int branching_point = -1;
  double shift{0.0};
  for (int i{0}, idx = branching_candidates.min();
       i < branching_candidates.size();
       ++i, idx = branching_candidates.next(idx)) {
    const double mid{(*box)[i].mid()};
    shift = p[i] - mid;
    const double abs_shift{std::abs(shift)};
    DREAL_LOG_TRACE(
        "BRANCHING: DIM {}, shift = {}, max_shift = {}, bisectable = {}",
        box->variable(i), shift, max_shift, (*box)[i].is_bisectable());
    if ((*box)[i].is_bisectable() && abs_shift > max_shift) {
      branching_point = i;
      max_shift = abs_shift;
    }
  }
  if (branching_point == -1) {
    DREAL_LOG_TRACE("FAIL TO BRANCH");
    return true;
  } else {
    DREAL_LOG_TRACE("BRANCH on {}", box->variable(branching_point));
    const pair<Box, Box> bisected_boxes{box->bisect(branching_point)};
    if (shift > 0.0) {
      stack->emplace_back(bisected_boxes.first, branching_point);
      stack->emplace_back(bisected_boxes.second, branching_point);
    } else {
      stack->emplace_back(bisected_boxes.second, branching_point);
      stack->emplace_back(bisected_boxes.first, branching_point);
    }
  }
  // 4. Check if P' satisfies the constraints.
  // 4.1. YES: Great, we've found a solution.
  // 4.2. NO: Goto 2
  // 4.3. STOP: If |P - P'| is below a threshold or the number of
  //            iterations is exceeded the max_iter.
  // 5. Using P', branch the box B.
  return false;
}
}  // namespace dreal
