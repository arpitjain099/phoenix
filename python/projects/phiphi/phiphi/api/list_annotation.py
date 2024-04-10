from sqlalchemy.types import TypeDecorator, TEXT, String
import json

class ListString(TypeDecorator):
    """Custom SQLAlchemy type for storing lists of strings."""
    impl = String(length=65535)  # Use String with a large length for TEXT-like behavior

    def process_bind_param(self, value, dialect):
        if value is not None:
            value = json.dumps(value)
        return value

    def process_result_value(self, value, dialect):
        if value is not None:
            value = json.loads(value)
        return value