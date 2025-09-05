import requests


# 発行されたトークン
ACCESS_TOKEN = "HS0LaxNcPmsT60g82cqDwVydslqGoNbLK1rAGFPhBxB"

headers = {"Authorization": f"Bearer {ACCESS_TOKEN}"}

data = {
    "message": "こんにちは！\nLINE Notifyを使ってメッセージを送ってみたよ！"
}

requests.post(
    "https://notify-api.line.me/api/notify",
    headers=headers,
    data=data,
)

print("bb")
