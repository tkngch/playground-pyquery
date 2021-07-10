from abc import ABC, abstractmethod

from pyquery.logical_plan.logical_plan import LogicalPlan


class OptimiserRule(ABC):
    @abstractmethod
    def optimise(self, plan: LogicalPlan) -> LogicalPlan:
        raise NotImplementedError
