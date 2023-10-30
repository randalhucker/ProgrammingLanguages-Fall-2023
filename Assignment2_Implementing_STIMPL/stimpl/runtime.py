from typing import Any, Tuple, Optional

from stimpl.expression import *
from stimpl.types import *
from stimpl.errors import *

"""
Interpreter State
"""


class State(object):
    def __init__(
        self,
        variable_name: str,
        variable_value: Expr,
        variable_type: Type,
        next_state: "State",
    ) -> None:
        self.variable_name = variable_name
        self.value = (variable_value, variable_type)
        self.next_state = next_state

    def copy(self) -> "State":
        variable_value, variable_type = self.value
        return State(self.variable_name, variable_value, variable_type, self.next_state)

    def set_value(self, variable_name, variable_value, variable_type):
        return State(variable_name, variable_value, variable_type, self)

    def get_value(self, variable_name) -> Any:
        # First, check to see if the variable is in the current state.
        if variable_name == self.variable_name:
            # If it is, return the value.
            return self.value
        # Otherwise, check the next state.
        else:
            # If the variable_name is not this state, go to the next state and repeat.
            return self.next_state.get_value(variable_name)

    def __repr__(self) -> str:
        return f"{self.variable_name}: {self.value}, " + repr(self.next_state)


class EmptyState(State):
    def __init__(self):
        pass

    def copy(self) -> "EmptyState":
        return EmptyState()

    def get_value(self, variable_name) -> None:
        return None

    def __repr__(self) -> str:
        return ""


def InitCommonExpression(
    state, left, right
) -> Tuple[Any | None, Type, Any | None, Type, State]:
    left_result, left_type, new_state = evaluate(left, state)
    right_result, right_type, newer_state = evaluate(right, new_state)
    return (left_result, left_type, right_result, right_type, newer_state)


"""
Main evaluation logic!
"""


def evaluate(expression: Expr, state: State) -> Tuple[Optional[Any], Type, State]:
    match expression:
        case Ren():
            return (None, Unit(), state)

        case IntLiteral(literal=l):
            return (l, Integer(), state)

        case FloatingPointLiteral(literal=l):
            return (l, FloatingPoint(), state)

        case StringLiteral(literal=l):
            return (l, String(), state)

        case BooleanLiteral(literal=l):
            return (l, Boolean(), state)

        case Print(to_print=to_print):
            printable_value, printable_type, new_state = evaluate(to_print, state)

            match printable_type:
                case Unit():
                    print("Unit")
                case _:
                    print(f"{printable_value}")

            return (printable_value, printable_type, new_state)

        case Sequence(exprs=exprs) | Program(exprs=exprs):
            result = None  # Initialize result to None.
            type = Unit()  # Initialize type to Unit.
            for expr in exprs:  # For each expression in the sequence...
                result, type, new_state = evaluate(
                    expr, state
                )  # Evaluate the expression.
                state = new_state  # Update the state.
            return (
                result,
                type,
                state,
            )  # Return the result of the last expression. Including the result, type, and state.

        case Variable(variable_name=variable_name):
            value = state.get_value(variable_name)
            if value == None:
                raise InterpSyntaxError(
                    f"Cannot read from {variable_name} before assignment."
                )
            variable_value, variable_type = value
            return (variable_value, variable_type, state)

        case Assign(variable=variable, value=value):
            value_result, value_type, new_state = evaluate(value, state)

            variable_from_state = new_state.get_value(variable.variable_name)
            _, variable_type = (
                variable_from_state if variable_from_state else (None, None)
            )

            if value_type != variable_type and variable_type != None:
                raise InterpTypeError(
                    f"""Mismatched types for Assignment:
            Cannot assign {value_type} to {variable_type}"""
                )

            new_state = new_state.set_value(
                variable.variable_name, value_result, value_type
            )
            return (value_result, value_type, new_state)

        case Add(left=left, right=right):
            result = 0
            left_result, left_type, new_state = evaluate(left, state)
            right_result, right_type, new_state = evaluate(right, new_state)

            if left_type != right_type:
                raise InterpTypeError(
                    f"""Mismatched types for Add:
            Cannot add {left_type} to {right_type}"""
                )

            match left_type:
                case Integer() | String() | FloatingPoint():
                    result = left_result + right_result
                case _:
                    raise InterpTypeError(f"""Cannot add {left_type}s""")

            return (result, left_type, new_state)

        case Subtract(left=left, right=right):
            # Initialize result to 0.
            result = 0
            # Evaluate the left and right expressions. Get the results, types, and new state.
            (
                left_result,
                left_type,
                right_result,
                right_type,
                new_state,
            ) = InitCommonExpression(state, left, right)

            # If the left and right types are not the same, raise an error.
            if left_type != right_type:
                raise InterpTypeError(
                    f"""Mismatched types for Subtract:
            Cannot subtract {left_type} to {right_type}"""
                )

            # Match the left type.
            match left_type:
                # If the type is Integer or FloatingPoint, perform the subtraction. Semantics rule 6.
                case Integer() | FloatingPoint():
                    result = left_result - right_result
                # If the type is Not Integer or FloatingPoint, raise error.
                case _:
                    raise InterpTypeError(f"""Cannot subtract {left_type}s""")
            # Return the result, left type, and new state.
            return (result, left_type, new_state)

        case Multiply(left=left, right=right):
            # Initialize result to 0.
            result = 0
            # Evaluate the left and right expressions. Get the results, types, and new state.
            (
                left_result,
                left_type,
                right_result,
                right_type,
                new_state,
            ) = InitCommonExpression(state, left, right)

            # If the left and right types are not the same, raise an error.
            if left_type != right_type:
                raise InterpTypeError(
                    f"""Mismatched types for Multiply:
            Cannot multiply {left_type} to {right_type}"""
                )

            # Match the left type.
            match left_type:
                # If the type is Integer or FloatingPoint, perform the multiplication. Semantics rule 6.
                case Integer() | FloatingPoint():
                    result = left_result * right_result
                # If the type is Not Integer or FloatingPoint, raise error.
                case _:
                    raise InterpTypeError(f"""Cannot multiply {left_type}s""")
            # Return the result, left type, and new state.
            return (result, left_type, new_state)

        case Divide(left=left, right=right):
            # Initialize result to 0.
            result = 0
            # Evaluate the left and right expressions. Get the results, types, and new state.
            (
                left_result,
                left_type,
                right_result,
                right_type,
                new_state,
            ) = InitCommonExpression(state, left, right)

            # If the left and right types are not the same, raise an error.
            if left_type != right_type:
                raise InterpTypeError(
                    f"""Mismatched types for Divide:
            Cannot divide {left_type} to {right_type}"""
                )

            # Match the left type.
            match left_type:
                # If the type is Integer or FloatingPoint, perform the division.
                case Integer() | FloatingPoint():
                    if right_result == 0:
                        raise InterpMathError(f"""Cannot divide by zero""")
                    # Do integer division if both operands are integers. Semantics rule 7.
                    if left_type == Integer():
                        result = left_result // right_result
                    else:
                        result = left_result / right_result
                # If the type is Not Integer or FloatingPoint, raise error.
                case _:
                    raise InterpTypeError(f"""Cannot divide {left_type}s""")
            # Return the result, left type, and new state.
            return (result, left_type, new_state)

        case And(left=left, right=right):
            (
                left_result,
                left_type,
                right_result,
                right_type,
                new_state,
            ) = InitCommonExpression(state, left, right)

            if left_type != right_type:
                raise InterpTypeError(
                    f"""Mismatched types for And:
            Cannot add {left_type} to {right_type}"""
                )
            match left_type:
                case Boolean():
                    result = left_result and right_result
                case _:
                    raise InterpTypeError(
                        "Cannot perform logical and on non-boolean operands."
                    )

            return (result, left_type, new_state)

        case Or(left=left, right=right):
            # Evaluate the left and right expressions. Get the results, types, and new state.
            (
                left_result,
                left_type,
                right_result,
                right_type,
                new_state,
            ) = InitCommonExpression(state, left, right)

            # If the left and right types are not the same, raise an error.
            if left_type != right_type:
                raise InterpTypeError(
                    f"""Mismatched types for Or:
            Cannot add {left_type} to {right_type}"""
                )

            # Match the left type.
            match left_type:
                # If the type is Boolean, perform the logical or.
                case Boolean():
                    result = left_result or right_result
                # If the type is Not Bool, raise error.
                case _:
                    raise InterpTypeError(
                        "Cannot perform logical or on non-boolean operands."
                    )

            # Return the result, Boolean type, and new state.
            return (result, left_type, new_state)

        case Not(expr=expr):
            # Evaluate the expression. Get the expression value, type, and new state.
            expr_value, expr_type, new_state = evaluate(expr, state)
            # Match the expression type.
            match expr_type:
                # If the type is Boolean, perform the logical not.
                case Boolean():
                    result = not expr_value
                # If the type is Not Bool, raise error.
                case _:
                    raise InterpTypeError(
                        "Cannot perform logical not on non-boolean operands."
                    )

            # Return the result, Boolean type, and new state.
            return (result, expr_type, new_state)

        case If(condition=condition, true=true, false=false):
            # Evaluate the condition. Get the condition value, type, and new state.
            condition_value, condition_type, new_state = evaluate(condition, state)

            # If the condition is not a boolean, raise an error. Type rule 8.
            if condition_type != Boolean():
                raise InterpTypeError(
                    "Cannot perform logical if on non-boolean operands."
                )

            # If the condition is true, evaluate the true branch. Semantics rule 13.
            if condition_value:
                return evaluate(true, new_state)
            else:
                return evaluate(false, new_state)

        case Lt(left=left, right=right):
            (
                left_result,
                left_type,
                right_result,
                right_type,
                new_state,
            ) = InitCommonExpression(state, left, right)

            result = None

            if left_type != right_type:
                raise InterpTypeError(
                    f"""Mismatched types for Lt:
            Cannot compare {left_type} to {right_type}"""
                )

            match left_type:
                case Integer() | Boolean() | String() | FloatingPoint():
                    result = left_result < right_result
                case Unit():
                    result = False
                case _:
                    raise InterpTypeError(f"Cannot perform < on {left_type} type.")

            return (result, Boolean(), new_state)

        case Lte(left=left, right=right):
            # Get the left and right results, types, and new state.
            (
                left_result,
                left_type,
                right_result,
                right_type,
                new_state,
            ) = InitCommonExpression(state, left, right)

            result = None

            # If the left and right types are not the same, raise an error.
            if left_type != right_type:
                raise InterpTypeError(
                    f"""Mismatched types for Lte:
            Cannot compare {left_type} to {right_type}"""
                )

            # Match the left/right type.
            match left_type:
                # If the type is Integer, Boolean, String, or FloatingPoint, perform the comparison.
                case Integer() | Boolean() | String() | FloatingPoint():
                    result = left_result <= right_result
                # If the type is Unit, return True.
                case Unit():
                    result = True
                case _:
                    raise InterpTypeError(f"Cannot perform <= on {left_type} type.")
            # Return the result, Boolean type, and new state.
            return (result, Boolean(), new_state)

        case Gt(left=left, right=right):
            # Get the left and right results, types, and new state.
            (
                left_result,
                left_type,
                right_result,
                right_type,
                new_state,
            ) = InitCommonExpression(state, left, right)

            result = None

            # If the left and right types are not the same, raise an error.
            if left_type != right_type:
                raise InterpTypeError(
                    f"""Mismatched types for Gt:
            Cannot compare {left_type} to {right_type}"""
                )

            # Match the left/right type.
            match left_type:
                # If the type is Integer, Boolean, String, or FloatingPoint, perform the comparison.
                case Integer() | Boolean() | String() | FloatingPoint():
                    result = left_result > right_result
                # If the type is Unit, return False.
                case Unit():
                    result = False
                case _:
                    raise InterpTypeError(f"Cannot perform > on {left_type} type.")
            # Return the result, Boolean type, and new state.
            return (result, Boolean(), new_state)

        case Gte(left=left, right=right):
            # Get the left and right results, types, and new state.
            (
                left_result,
                left_type,
                right_result,
                right_type,
                new_state,
            ) = InitCommonExpression(state, left, right)

            result = None

            # If the left and right types are not the same, raise an error.
            if left_type != right_type:
                raise InterpTypeError(
                    f"""Mismatched types for Gte:
            Cannot compare {left_type} to {right_type}"""
                )

            # Match the left/right type.
            match left_type:
                # If the type is Integer, Boolean, String, or FloatingPoint, perform the comparison.
                case Integer() | Boolean() | String() | FloatingPoint():
                    result = left_result >= right_result
                # If the type is Unit, return True.
                case Unit():
                    result = True
                case _:
                    raise InterpTypeError(f"Cannot perform >= on {left_type} type.")
            # Return the result, Boolean type, and new state.
            return (result, Boolean(), new_state)

        case Eq(left=left, right=right):
            # Get the left and right results, types, and new state.
            (
                left_result,
                left_type,
                right_result,
                right_type,
                new_state,
            ) = InitCommonExpression(state, left, right)

            result = None
            # If the left and right types are not the same, raise an error.
            if left_type != right_type:
                raise InterpTypeError(
                    f"""Mismatched types for Eq:
            Cannot compare {left_type} to {right_type}"""
                )

            # Match the left/right type.
            match left_type:
                # If the type is Integer, Boolean, String, or FloatingPoint, perform the comparison.
                case Integer() | Boolean() | String() | FloatingPoint():
                    result = left_result == right_result
                # If the type is Unit, return True.
                case Unit():
                    result = True
                case _:
                    raise InterpTypeError(f"Cannot perform == on {left_type} type.")
            # Return the result, Boolean type, and new state.
            return (result, Boolean(), new_state)

        case Ne(left=left, right=right):
            # Get the left and right results, types, and new state.
            (
                left_result,
                left_type,
                right_result,
                right_type,
                new_state,
            ) = InitCommonExpression(state, left, right)

            result = None
            # If the left and right types are not the same, raise an error.
            if left_type != right_type:
                raise InterpTypeError(
                    f"""Mismatched types for Ne:
            Cannot compare {left_type} to {right_type}"""
                )

            # Match the left/right type.
            match left_type:
                # If the type is Integer, Boolean, String, or FloatingPoint, perform the comparison.
                case Integer() | Boolean() | String() | FloatingPoint():
                    result = left_result != right_result
                # If the type is Unit, return False.
                case Unit():
                    result = False
                case _:
                    raise InterpTypeError(f"Cannot perform != on {left_type} type.")
            # Return the result, Boolean type, and new state.
            return (result, Boolean(), new_state)

        case While(condition=condition, body=body):
            condition_value = None  # Initialize condition_value to None.
            condition_type = Unit()  # Initialize condition_type to Unit.
            condition_value, condition_type, new_state = evaluate(
                condition, state
            )  # Evaluate the condition.

            if condition_type != Boolean():
                # If the condition is not a boolean, raise an error. Type rule 8.
                raise InterpTypeError(
                    "Cannot perform logical while on non-boolean operands."
                )

            # While the condition is true, evaluate the body. Semantics rule 12.
            while condition_value:
                _, _, new_state = evaluate(
                    body, new_state
                )  # Evaluate the body and update the state.
                condition_value, condition_type, new_state = evaluate(
                    condition, new_state
                )

            # Return the final state, value, and type.
            return (condition_value, condition_type, new_state)

        case _:
            raise InterpSyntaxError("Unhandled!")
    pass


def run_stimpl(program, debug=False):
    state = EmptyState()
    program_value, program_type, program_state = evaluate(program, state)

    if debug:
        print(f"program: {program}")
        print(f"final_value: ({program_value}, {program_type})")
        print(f"final_state: {program_state}")

    return program_value, program_type, program_state
