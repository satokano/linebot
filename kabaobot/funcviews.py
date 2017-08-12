from django.conf import settings
from rest_framework.decorators import api_view, permission_classes
from rest_framework import permissions
from rest_framework.response import Response
import logging
import json
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

line_bot_api = LineBotApi(settings.CHANNEL_ACCESS_TOKEN)
whhandler = WebhookHandler(settings.CHANNEL_SECRET)

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

        try:
            whhandler.handle(body_unicode, signature)
        except InvalidSignatureError as ise:
            logger.error("[LC] InvalidSignatureError")
            raise # rethrow

    except Exception as ee:
        logger.exception("[LC] exception::")
    finally:
        logger.info("[LC] callback end")
        return Response("OK")

@whhandler.add(MessageEvent, message=TextMessage)
def message_text(event):
    logger = logging.getLogger('linecallbacklogger')
    logger.info("[LC] start handling TextMessage")
    line_bot_api.reply_message(event.reply_token, TextSendMessage(text=event.message.text))
    logger.info("[LC] end handling TextMessage")

