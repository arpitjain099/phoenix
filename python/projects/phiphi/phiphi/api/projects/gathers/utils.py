"""Utils for the gather."""
import pydantic


def validate_dependency(dependency_key: str):  # type: ignore[no-untyped-def]
    """Utility function to validate dependency between one attribute and an other.

    For example, if attribute_1 is set, the attribute_2 should be None.

    This would be added to a pydantic model like this:
    ```
    _validate_dependency_<attribute_1> = pydantic.field_validator(
        "<attribute_1>"
    )(utils.validate_dependency("<attribute_2>"))
    ```

    Args:
        dependency_key (str): The key of the attribute that should be None.
    """

    def fn(cls, v, info: pydantic.ValidationInfo):  # type: ignore[no-untyped-def]
        if v is not None and info.data[dependency_key] is not None:
            raise ValueError(
                f"{info.field_name} can only be set if {dependency_key} is not set (None)"
            )

        return v

    return fn
