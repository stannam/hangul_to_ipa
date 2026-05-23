from flask import Flask

app = Flask(__name__)

APP_NAME = "Hangul to IPA"
NEW_URL = "https://h2ipa.stanleynam.ca/"

@app.route("/")
def index():
    return f"""
    <!doctype html>
    <html>
    <head>
        <meta charset="utf-8">
        <meta http-equiv="refresh" content="5; url={NEW_URL}">
        <title>{APP_NAME} has moved</title>
    </head>
    <body style="font-family: sans-serif; max-width: 700px; margin: 4rem auto; line-height: 1.6;">
        <h1>Hangul to IPA has moved</h1>
        <h1>Hangul to IPA의 새주소</h1>
        <p>
            This app is now available at: / 이제 아래 주소로 들어오세요.
            <a href="{NEW_URL}">{NEW_URL}</a>
        </p>
        <p>You will be redirected in 5 seconds. / 5초 후 이동합니다.</p>
    </body>
    </html>
    """