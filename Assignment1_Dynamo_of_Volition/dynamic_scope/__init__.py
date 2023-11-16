from typing import Dict, Any, Iterator, Optional
from collections import abc
from types import FunctionType
import inspect


class DynamicScope(abc.Mapping):
    """This class is used to create a dynamic scope for a function. It is used to get the local variables of the function and the variables that are defined in the parent scope. It is also used to check if a variable is defined in the local scope or not.

    Args:
        abc (Mapping): This was the predefined class that was mentioned in the assignment.
    """

    def __init__(self, local_vars: Dict[str, Optional[Any]]):
        # This is the dictionary that will be used to store the local variables of the function.
        self.env_vars: Dict[str, Optional[Any]] = local_vars
        # This is the list that will be used to store the variables that are not defined (unbound) in the local scope.
        self.unbound_vars: list[str] = []

    def __getitem__(self, key):
        # This is used to check if the variable was unbound at any point in time when building the scope list.
        if key in self.unbound_vars:
            raise UnboundLocalError(
                f"local variable '{key}' referenced before assignment"
            )
        # This is used to check if the variable is defined in the parent scope or not.
        try:
            return self.env_vars[key]
        # This is used to raise an error if the variable is not defined in the local scope or the parent scope.
        except KeyError:
            raise NameError(f"Name '{key}' is not defined.")

    def __setitem__(self, key, value):
        # Per the assignment, if the variable is already defined in the local scope, then it should not be updated.
        if key not in self.env_vars:
            self.env_vars[key] = value

    def __iter__(self):
        # This is used to iterate over the local variables of the function.
        return iter(self.env_vars)

    def __len__(self):
        # This is used to get the length of the local variables of the function.
        return len(self.env_vars)


def get_dynamic_re() -> DynamicScope:
    """This is the required function that will be used to get the dynamic scope of the function that is calling this function.

    Returns:
        DynamicScope: The class that was defined above. It is used to get the local variables of the function and the variables that are defined in the parent scope. It is also used to check if a variable is defined in the local scope or not.
    """
    ds = DynamicScope({})

    # Get the stack information of the function that is calling this function.
    stack_info = inspect.stack()
    # Remove the first element of the stack information because it is the function that is calling this function.
    stack_info.pop(0)

    for frame_info in stack_info:
        # Get the local variables, free variables, and unbound variables of the function that is calling this function.
        local_vars = frame_info.frame.f_locals
        free_vars = list(frame_info.frame.f_code.co_freevars)
        unbound_vars = list(frame_info.frame.f_code.co_varnames) + list(
            frame_info.frame.f_code.co_cellvars
        )

        for unbound_var in unbound_vars:
            # If the variable is defined in the local scope (after a call is made to the variable), then it is unbound.
            if (
                unbound_var not in free_vars
                and unbound_var not in local_vars
                and unbound_var not in ds.unbound_vars
            ):
                # Add the unbound variable to the list of unbound variables.
                ds.unbound_vars.append(unbound_var)

        for var_name in local_vars:
            # If the variable is not defined in the parent scope, and it is defined in the local scope.
            if var_name not in free_vars:
                # Add the variable to the local variables of the function.
                ds[var_name] = local_vars[var_name]
    return ds
