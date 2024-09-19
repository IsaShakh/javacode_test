from rest_framework.views import exception_handler as custom_exception_handler
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import ValidationError

def exception_handler(exc, context):
    response = custom_exception_handler(exc, context)
    if response is None:
        return Response({"detail": "Internal server error."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    if isinstance(exc, ValidationError):
        return Response({"detail": "Невалидный JSON", "errors": response.data}, status=status.HTTP_400_BAD_REQUEST)

    return response
