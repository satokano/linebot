from django.conf import settings
from rest_framework.decorators import api_view, permission_classes
from rest_framework import permissions
from rest_framework.response import Response
import logging
import json
import tempfile
import http.client, urllib.request, urllib.parse, urllib.error, base64
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, FollowEvent, UnfollowEvent, JoinEvent, LeaveEvent, PostbackEvent, BeaconEvent, TextMessage, ImageMessage, VideoMessage, AudioMessage, LocationMessage, StickerMessage, TextSendMessage
import cloudinary
import cloudinary.uploader
import cloudinary.api

line_bot_api = LineBotApi(settings.CHANNEL_ACCESS_TOKEN)
whhandler = WebhookHandler(settings.CHANNEL_SECRET)
cognitive_subscription_key = settings.COGNITIVE_SUBSCRIPTION_KEY
cognitive_uri_base = 'westcentralus.api.cognitive.microsoft.com'
cognitive_headers = {
    'Content-Type': 'application/json',
    'Ocp-Apim-Subscription-Key': cognitive_subscription_key,
}
cognitive_params = urllib.parse.urlencode({
    'visualFeatures': 'Categories,Tags,Description,Faces,Adult',
    'language': 'en',
})

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
            # LINE以外からと考えられるのでOK以外のレスポンスでもよいかも
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

@whhandler.add(MessageEvent, message=ImageMessage)
def message_image(event):
    logger = logging.getLogger('linecallbacklogger')
    logger.info("[LC] start handling ImageMessage")
    #line_bot_api.reply_message(event.reply_token, TextSendMessage(text="画像きた " + event.message.id))
    result = ""
    cognitive_result = ""
    message_content = line_bot_api.get_message_content(event.message.id)
    with tempfile.NamedTemporaryFile(delete=False) as fd:
        for chunk in message_content.iter_content():
            fd.write(chunk)
        fd.seek(0)
        #logger.info("[LC] temporary file name: " + fd.name)
        result = cloudinary.uploader.upload(fd.name)

    logger.info(result['url'])

    try:
        cognitive_body = "{'url': '%s'}" % result['url']
        conn = http.client.HTTPSConnection(cognitive_uri_base)
        conn.request("POST", "/vision/v1.0/analyze?%s" % cognitive_params, cognitive_body, cognitive_headers)
        response = conn.getresponse()
        data = response.read()
        parsed = json.loads(data)
        cognitive_result = json.dumps(parsed, sort_keys=True, indent=2)
    except Exception as e:
        logger.exception("[LC] MS Cognitive Service API Error::")

    line_bot_api.reply_message(event.reply_token, TextSendMessage(text="画像どうも " + result['url'] + "\n" + cognitive_result))
    logger.info("[LC] end handling ImageMessage")

@whhandler.add(MessageEvent, message=VideoMessage)
def message_video(event):
    logger = logging.getLogger('linecallbacklogger')
    logger.info("[LC] start handling VideoMessage")
    line_bot_api.reply_message(event.reply_token, TextMessage(text="動画ありがとう"))
    logger.info("[LC] end handling VideoMessage")

@whhandler.add(MessageEvent, message=AudioMessage)
def message_audio(event):
    logger = logging.getLogger('linecallbacklogger')
    logger.info("[LC] start handling AudioMessage")
    line_bot_api.reply_message(event.reply_token, TextMessage(text="音声ありがとう"))
    logger.info("[LC] end handling AudioMessage")

# PythonのSDKにFileMessageが存在しない気がする
# https://github.com/line/line-bot-sdk-python/blob/master/linebot/models/messages.py
#@whhandler.add(MessageEvent, message=FileMessage)
def message_file(event):
    logger = logging.getLogger('linecallbacklogger')
    logger.info("[LC] FileMessage")

@whhandler.add(MessageEvent, message=LocationMessage)
def message_location(event):
    logger = logging.getLogger('linecallbacklogger')
    logger.info("[LC] start handling LocationMessage")
    line_bot_api.reply_message(event.reply_token, TextMessage(text="そんなところに"))
    logger.info("[LC] end handling LocationMessage")

@whhandler.add(MessageEvent, message=StickerMessage)
def message_sticker(event):
    logger = logging.getLogger('linecallbacklogger')
    logger.info("[LC] start handling StickerMessage")
    line_bot_api.reply_message(event.reply_token, TextMessage(text="(´・ω・｀)"))
    logger.info("[LC] end handling StickerMessage")

@whhandler.add(FollowEvent)
def follow(event):
    logger = logging.getLogger('linecallbacklogger')
    logger.info("[LC] follow event")
    line_bot_api.reply_message(event.reply_token, TextSendMessage(text="フォローありがとうございます"))

@whhandler.add(UnfollowEvent)
def unfollow(event):
    logger = logging.getLogger('linecallbacklogger')
    logger.info("[LC] unfollow event")

@whhandler.add(JoinEvent)
def join(event):
    logger = logging.getLogger('linecallbacklogger')
    logger.info("[LC] join event")
    line_bot_api.reply_message(event.reply_token, TextSendMessage(text="こんにちは"))

@whhandler.add(LeaveEvent)
def leave(event):
    logger = logging.getLogger('linecallbacklogger')
    logger.info("[LC] leave event")

@whhandler.add(PostbackEvent)
def postback(event):
    logger = logging.getLogger('linecallbacklogger')
    logger.info("[LC] postback event")

@whhandler.add(BeaconEvent)
def beacon(event):
    logger = logging.getLogger('linecallbacklogger')
    logger.info("[LC] beacon event")

