from rest_framework.decorators import api_view, permission_classes
from rest_framework import permissions
from rest_framework.response import Response
import logging

@api_view(('GET',))
@permission_classes((permissions.AllowAny,))
def hello_world(request):
    return Response({"message": "Hello, World!"})

@api_view(('GET','POST',))
@permission_classes((permissions.AllowAny,))
def linecallback(request):
    logger = logging.getLogger('linecallbacklogger')
    logger.info("[LC] callback start")

    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    logger.info("[LC] Request body: " + body)

    logger.info("[LC] callback end")
    return Response("OK")

