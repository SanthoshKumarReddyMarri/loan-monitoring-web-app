from rest_framework.views import exception_handler


def custom_exception_handler(exc, context):
    """
    Global exception handler that returns a consistent API response format.
    """
    response = exception_handler(exc, context)

    if response is None:
        return response

    message = "Request failed."

    if isinstance(response.data, dict):
        message = response.data.get("detail", message)

    response.data = {
        "success": False,
        "message": message,
        "errors": response.data,
    }

    return response