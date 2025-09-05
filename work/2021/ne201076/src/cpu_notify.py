import requests

url = 'https://notify-api.line.me/api/notify'#LINE NotifyのAPIのURL
token = '2RNdAKwlaj69HK0KlEdMX1y575gDWNKrPpggFcLnh82' #自分のアクセストークン
ms = "新たなソフトを開くと負担が過剰にかかってしまいます。"#送信する通知内容

def line(message,url,token):
    post_data = {'message': message}
    headers = {'Authorization': 'Bearer ' + token}
    #送信する
    res = requests.post(url,
                        data=post_data,
                        headers=headers)
    print(res.text)#メッセージが送信されたかどうかの確認

while True:
    now=dt.('cpu_temps')
    dt = getCpuTempFromFile(data_file) #CPU温度取得
    print(cpu_temps)
    if print(cpu_temp) == "print >= 80":#CPU温度が80度以上の際にラインが送られるようにする
        line(postdate=message, date=postdate, palams=postdate　)#lineを呼び出す
        break
    time.sleep(1)
