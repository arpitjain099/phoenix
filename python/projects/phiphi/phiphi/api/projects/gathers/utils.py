"""Utils for the gather."""
from typing import Any, Callable

import pydantic


def validate_both_not_set(attribute_2: str) -> Callable[[Any, Any, pydantic.ValidationInfo], Any]:
    """Utility function to validate both attributes are not set.

    For example, if attribute_1 is set, the attribute_2 should be None.

    This would be added to a pydantic model like this:
    ```
    _validate_dependency_<attribute_1> = pydantic.field_validator(
        "<attribute_1>"
    )(utils.validate_dependency("<attribute_2>"))
    ```

    Args:
        attribute_2 (str): The attribute that should be None.
    """

    def fn(cls: Any, v: Any, info: pydantic.ValidationInfo) -> Any:
        if v is not None and info.data[attribute_2] is not None:
            raise ValueError(
                f"{info.field_name} can only be set if {attribute_2} is not set (None)"
            )

        return v

    return fn
