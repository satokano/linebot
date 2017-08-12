from rest_framework.decorators import api_view, permission_classes
from rest_framework import permissions
from rest_framework.response import Response
import logging
import json

@api_view(('GET',))
@permission_classes((permissions.AllowAny,))
def hello_world(request):
    return Response({"message": "Hello, World!"})

@api_view(('GET','POST',))
@permission_classes((permissions.AllowAny,))
def linecallback(request):
    logger = logging.getLogger('linecallbacklogger')
    logger.info("[LC] callback start")

    try:
        signature = request.META['HTTP_X_LINE_SIGNATURE']
        logger.info("[LC] signature: " + signature)
        body_unicode = request.body.decode('utf-8')
        body_data = json.loads(body_unicode)
        logger.info("[LC] Request body: " + json.dumps(body_data))




    except Exception as ee:
        logger.exception("[LC] exception::")
    finally:
        logger.info("[LC] callback end")
        return Response("OK")

