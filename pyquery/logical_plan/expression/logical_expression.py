from abc import ABC, abstractmethod

from pyquery.datatypes import Field
from pyquery.logical_plan.logical_plan import LogicalPlan
from pyquery.physical_plan.expression.physical_expression import PhysicalExpression


class LogicalExpression(ABC):
    @abstractmethod
    def to_field(self, plan: LogicalPlan) -> Field:
        raise NotImplementedError

    @abstractmethod
    def to_string(self) -> str:
        raise NotImplementedError

    @abstractmethod
    def to_physical_expression(self, plan: LogicalPlan) -> PhysicalExpression:
        raise NotImplementedError

    def eq(self, right: "LogicalExpression") -> "LogicalExpression":
        from pyquery.logical_plan.expression.boolean.logical_eq import LogicalEq

        return LogicalEq(self, right)

    def neq(self, right: "LogicalExpression") -> "LogicalExpression":
        from pyquery.logical_plan.expression.boolean.logical_neq import LogicalNeq

        return LogicalNeq(self, right)

    def gt(self, right: "LogicalExpression") -> "LogicalExpression":
        from pyquery.logical_plan.expression.boolean.logical_gt import LogicalGt

        return LogicalGt(self, right)

    def gteq(self, right: "LogicalExpression") -> "LogicalExpression":
        from pyquery.logical_plan.expression.boolean.logical_gt_eq import LogicalGtEq

        return LogicalGtEq(self, right)

    def lt(self, right: "LogicalExpression") -> "LogicalExpression":
        from pyquery.logical_plan.expression.boolean.logical_lt import LogicalLt

        return LogicalLt(self, right)

    def lteq(self, right: "LogicalExpression") -> "LogicalExpression":
        from pyquery.logical_plan.expression.boolean.logical_lt_eq import LogicalLtEq

        return LogicalLtEq(self, right)

    def add(self, right: "LogicalExpression") -> "LogicalExpression":
        from pyquery.logical_plan.expression.math.logical_add import LogicalAdd

        return LogicalAdd(self, right)

    def divide(self, right: "LogicalExpression") -> "LogicalExpression":
        from pyquery.logical_plan.expression.math.logical_divide import LogicalDivide

        return LogicalDivide(self, right)

    def modulus(self, right: "LogicalExpression") -> "LogicalExpression":
        from pyquery.logical_plan.expression.math.logical_modulus import LogicalModulus

        return LogicalModulus(self, right)

    def multiply(self, right: "LogicalExpression") -> "LogicalExpression":
        from pyquery.logical_plan.expression.math.logical_multiply import (
            LogicalMultiply,
        )

        return LogicalMultiply(self, right)

    def subtract(self, right: "LogicalExpression") -> "LogicalExpression":
        from pyquery.logical_plan.expression.math.logical_subtract import (
            LogicalSubtract,
        )

        return LogicalSubtract(self, right)

    def alias(self, alias: str) -> "LogicalExpression":
        from pyquery.logical_plan.expression.logical_alias import LogicalAlias

        return LogicalAlias(self, alias)

    def and_(self, right: "LogicalExpression") -> "LogicalExpression":
        from pyquery.logical_plan.expression.boolean.logical_and import LogicalAnd

        return LogicalAnd(self, right)

    def or_(self, right: "LogicalExpression") -> "LogicalExpression":
        from pyquery.logical_plan.expression.boolean.logical_or import LogicalOr

        return LogicalOr(self, right)
