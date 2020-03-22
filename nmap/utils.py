import ast
import os


def env(key, default=None, required=False, value_type=None):
    """
    Retrieves environment variables and returns Python natives. The (optional)
    default will be returned if the environment variable does not exist.
    """
    try:
        value = os.environ[key]
        value = ast.literal_eval(value)
    except (SyntaxError, ValueError):
        pass
    except KeyError:
        if default is not None or not required:
            return default
        raise Exception("Missing required environment variable '%s'" % key)

    if value_type is None:
        if default is not None:
            value_type = default.__class__

    if value_type is None:
        return value
    elif isinstance(value, value_type):
        return value
    elif issubclass(value_type, list):
        if isinstance(value, tuple):
            return list(value)
        else:
            value = str(value).strip()
            if not value:
                return []
            else:
                return value.split(",")
    elif issubclass(value_type, tuple):
        if isinstance(value, list):
            return tuple(value)
        else:
            value = str(value).strip()
            if not value:
                return tuple()
            else:
                return tuple(value.split(","))
    elif issubclass(value_type, bool):
        value = str(value).strip()
        if not value:
            return False
        elif value.lower() == 'true':
            return True
        elif value.lower() == 'false':
            return False
        else:
            raise Exception("'{}' is a boolean environment variable, only accept value 'true' ,'false' and '' with case insensitive, but the configured value is '{}'".format(key, value))
    elif issubclass(value_type, int):
        return int(value)
    elif issubclass(value_type, float):
        return float(value)
    else:
        raise Exception("'{0}' is a {1} environment variable, but {1} is not supported now".format(key, value_type))
