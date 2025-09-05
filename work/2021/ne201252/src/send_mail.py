#import smtplib
#from email.mime.text import MIMEText
#from email.utils import formatdate

#sendAddress = 'ne201252@senshu-u.jp'
#password = ''

#subject = '警告'
#bodyText = '車に乗っていると判断できる加速度が検知されました。ながら運転は危険ですのですぐにスマートフォンの使用をやめてください。'
#fromAddress = 'ne201252@senshu-u.jp'
#toAddress = 'ne201252@senshu-u.jp'

# SMTPサーバに接続
#smtpobj = smtplib.SMTP('smtp.gmail.com', 587)
#smtpobj.starttls()
#smtpobj.login(sendAddress, password)

# メール作成
#msg = MIMEText(bodyText)
#msg['Subject'] = subject
#msg['From'] = fromAddress
#msg['To'] = toAddress
#msg['Date'] = formatdate()

# 作成したメールを送信
#smtpobj.send_message(msg)
#smtpobj.close()
