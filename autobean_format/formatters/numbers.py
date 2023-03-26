import copy
from autobean_refactor import models
from . import base


@base.formatter(models.UnaryOp)
def format_unary_op(unary_op: models.UnaryOp, context: base.Context) -> models.UnaryOp:
    return copy.deepcopy(unary_op)


@base.formatter(models.AddOp)
def format_add_op(add_op: models.AddOp, context: base.Context) -> models.AddOp:
    return copy.deepcopy(add_op)


@base.formatter(models.MulOp)
def format_mul_op(mul_op: models.MulOp, context: base.Context) -> models.MulOp:
    return copy.deepcopy(mul_op)


@base.formatter(models.LeftParen)
def format_left_paren(left_paren: models.LeftParen, context: base.Context) -> models.LeftParen:
    return copy.deepcopy(left_paren)


@base.formatter(models.RightParen)
def format_right_paren(right_paren: models.RightParen, context: base.Context) -> models.RightParen:
    return copy.deepcopy(right_paren)


@base.formatter(models.Number)
def format_number(number: models.Number, context: base.Context) -> models.Number:
    return copy.deepcopy(number)


@base.formatter(models.NumberExpr)
def format_number_expr(number_expr: models.NumberExpr, context: base.Context) -> models.NumberExpr:
    return models.NumberExpr.from_children(
        number_add_expr=base.format(number_expr.raw_number_add_expr, context),
    )


@base.formatter(models.NumberAddExpr)
def format_number_add_expr(number_add_expr: models.NumberAddExpr, context: base.Context) -> models.NumberAddExpr:
    return models.NumberAddExpr.from_children(
        operands=tuple(base.format_repeated(number_add_expr.raw_operands, context)),
        ops=tuple(base.format_repeated(number_add_expr.raw_ops, context)),
    )


@base.formatter(models.NumberMulExpr)
def format_number_mul_expr(number_mul_expr: models.NumberMulExpr, context: base.Context) -> models.NumberMulExpr:
    return models.NumberMulExpr.from_children(
        operands=tuple(base.format_repeated(number_mul_expr.raw_operands, context)),
        ops=tuple(base.format_repeated(number_mul_expr.raw_ops, context)),
    )


@base.formatter(models.NumberUnaryExpr)
def format_number_unary_expr(number_unary_expr: models.NumberUnaryExpr, context: base.Context) -> models.NumberUnaryExpr:
    return models.NumberUnaryExpr.from_children(
        unary_op=base.format(number_unary_expr.raw_unary_op, context),
        operand=base.format(number_unary_expr.raw_operand, context),
    )


@base.formatter(models.NumberParenExpr)
def format_number_paren_expr(number_paren_expr: models.NumberParenExpr, context: base.Context) -> models.NumberParenExpr:
    return models.NumberParenExpr.from_children(
        inner_expr=base.format(number_paren_expr.raw_inner_expr, context),
    )
