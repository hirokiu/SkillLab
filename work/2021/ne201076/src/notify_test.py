import requests

url = "https://notify-api.line.me/api/notify" #LINE NotifyのAPIのURL
token = '2RNdAKwlaj69HK0KlEdMX1y575gDWNKrPpggFcLnh82' #自分のアクセストークン
headers = {'Authorization': 'Bearer ' + token}

#送信する通知内容
message = 'これは薬師神が行っているテストになります。実際にCPU温度に反応しているわけではありません。これ以上新たにソフトを開くと、過剰に負荷がかかる恐れがあります。'
payload = {'message': message}

r = requests.post(url, headers=headers, params=payload,)
if r.status_code != 200:
    print("error : %d" % (r.status_code))
