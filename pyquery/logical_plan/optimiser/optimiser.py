from pyquery.logical_plan.logical_plan import LogicalPlan
from pyquery.logical_plan.optimiser.rule.projection_push_down_rule import (
    ProjectionPushDownRule,
)


class Optimiser:
    @staticmethod
    def optimise(plan: LogicalPlan) -> LogicalPlan:
        rule = ProjectionPushDownRule()
        return rule.optimise(plan)
