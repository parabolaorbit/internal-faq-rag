
def calculate(expression: str) -> float:
    """
    Evaluate a mathematical expression and return the result.

    Args:
        expression (str): A string containing a mathematical expression."""

    try:
        # Evaluate the expression using eval
        result = eval(expression, {"__builtins__": None}, {})
        return result


    except Exception as e:
        raise ValueError(f"Invalid expression: {expression}") from e
    