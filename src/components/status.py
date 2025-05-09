import functools
import inspect
from typing import Any, Callable, TypedDict

import streamlit as st


def return_stage_context(key: str) -> Callable[[Callable[..., Any]], Callable[..., dict[str, Any]]]:
    """Decorator to return a dictionary with a specific key and the result of the function.

    Args:
        key (str): The key to be used in the returned dictionary.

    """

    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            return {key: result}

        return wrapper

    return decorator


class Stage(TypedDict):
    """A dictionary representing a stage.

    Attributes:
        name (str): The name of the stage.
        func (Callable[..., dict[str, Any] | None]): The function to be executed
            for the stage. It should return a dictionary with the context or None.

    """

    name: str
    func: Callable[..., dict[str, Any] | None]


def stage_status(stages: list[Stage], context: dict[str, Any] | None = None) -> None:
    """Displays the status for few stages.

    Args:
        stages (list[Stage]): A list of stages to be executed.
        context (dict[str, Any] | None): A dictionary containing the context for the stages. Defaults to None.

    """
    with st.status("In progress...", expanded=True) as status:
        try:
            full_context = context.copy() if context else {}

            for stage in stages:
                func = stage["func"]
                func_kwargs = {
                    key: value for key, value in full_context.items() if key in inspect.signature(func).parameters
                }
                if new_context := func(**func_kwargs):
                    full_context.update(new_context)

                st.badge(stage["name"], color="green", icon=":material/check:")

            status.update(label="Successfully completed!", expanded=False)
        except Exception:
            st.badge(stage["name"], color="red", icon=":material/close:")
            status.update(label="An error occurred.")
            raise
