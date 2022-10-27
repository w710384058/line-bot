from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

app = Flask(__name__)

line_bot_api = LineBotApi('b5is7+yLL+ZSobACUxaCTaW5T7Gro7D6L89OCSkDdDG6wtPR1wU955DAaErAIN7aHGAKzo9vCXJP2rZcRPfLZCsjEl1qzbVsiN/t4hg9SrH6Om96cOCdqW3cU65IkM8W0BbtDTD7EMEM8tVhSLeDUAdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('3a1c58a70636fe3b6e0393ad593cf9e6')


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))


if __name__ == "__main__":
    app.run()