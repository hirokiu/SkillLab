import smtplib, ssl
from email.mime.text import MIMEText

def gmail1():
    # 以下にGmailの設定を書き込む★ --- (*1)
    gmail_account = "atsuri.snoopy@gmail.com"
    gmail_password = "11FlowBack26"
    # メールの送信先★ --- (*2)
    mail_to = "atsuri.snoopy@gmail.com"
    
    # メールデータ(MIME)の作成 --- (*3)
    subject = "パソコンの温度が高いです"
    body = "パソコンを休ませましょう"
    msg = MIMEText(body, "html")
    msg["Subject"] = subject
    msg["To"] = mail_to
    msg["From"] = gmail_account

    # Gmailに接続 --- (*4)
    server = smtplib.SMTP_SSL("smtp.gmail.com", 465,
        context=ssl.create_default_context())
    server.login(gmail_account, gmail_password)
    server.send_message(msg) # メールの送信
    print("ok.")

def gmail2():
    # 以下にGmailの設定を書き込む★ --- (*1)
    gmail_account = "atsuri.snoopy@gmail.com"
    gmail_password = "11FlowBack26"
    # メールの送信先★ --- (*2)
    mail_to = "atsuri.snoopy@gmail.com"
    
    # メールデータ(MIME)の作成 --- (*3)
    subject = "パソコンの温度が高いです"
    body = "アプリケーションなど使用していないものを消しましょう"
    msg = MIMEText(body, "html")
    msg["Subject"] = subject
    msg["To"] = mail_to
    msg["From"] = gmail_account

    # Gmailに接続 --- (*4)
    server = smtplib.SMTP_SSL("smtp.gmail.com", 465,
        context=ssl.create_default_context())
    server.login(gmail_account, gmail_password)
    server.send_message(msg) # メールの送信
    print("ok.")

def gmail3():
    # 以下にGmailの設定を書き込む★ --- (*1)
    gmail_account = "atsuri.snoopy@gmail.com"
    gmail_password = "11FlowBack26"
    # メールの送信先★ --- (*2)
    mail_to = "atsuri.snoopy@gmail.com"
    
    # メールデータ(MIME)の作成 --- (*3)
    subject = "パソコンの温度が高いです"
    body = "パソコンを休ませましょう。充電が50%未満なので、充電しましょう。"
    msg = MIMEText(body, "html")
    msg["Subject"] = subject
    msg["To"] = mail_to
    msg["From"] = gmail_account

    # Gmailに接続 --- (*4)
    server = smtplib.SMTP_SSL("smtp.gmail.com", 465,
        context=ssl.create_default_context())
    server.login(gmail_account, gmail_password)
    server.send_message(msg) # メールの送信
    print("ok.")

def gmail4():
    # 以下にGmailの設定を書き込む★ --- (*1)
    gmail_account = "atsuri.snoopy@gmail.com"
    gmail_password = "11FlowBack26"
    # メールの送信先★ --- (*2)
    mail_to = "atsuri.snoopy@gmail.com"
    
    # メールデータ(MIME)の作成 --- (*3)
    subject = "パソコンの温度が高いです"
    body = "アプリケーションなど使用していないものを消しましょう。充電が50%未満なので、充電しましょう。"
    msg = MIMEText(body, "html")
    msg["Subject"] = subject
    msg["To"] = mail_to
    msg["From"] = gmail_account

    # Gmailに接続 --- (*4)
    server = smtplib.SMTP_SSL("smtp.gmail.com", 465,
        context=ssl.create_default_context())
    server.login(gmail_account, gmail_password)
    server.send_message(msg) # メールの送信
    print("ok.")

def gmail5():
    # 以下にGmailの設定を書き込む★ --- (*1)
    gmail_account = "atsuri.snoopy@gmail.com"
    gmail_password = "11FlowBack26"
    # メールの送信先★ --- (*2)
    mail_to = "atsuri.snoopy@gmail.com"
    
    # メールデータ(MIME)の作成 --- (*3)
    subject = "パソコンの温度が高いです"
    body = "パソコンを休ませましょう。充電が50%未満なので、充電しましょう。画面も暗くしましょう。"
    msg = MIMEText(body, "html")
    msg["Subject"] = subject
    msg["To"] = mail_to
    msg["From"] = gmail_account

    # Gmailに接続 --- (*4)
    server = smtplib.SMTP_SSL("smtp.gmail.com", 465,
        context=ssl.create_default_context())
    server.login(gmail_account, gmail_password)
    server.send_message(msg) # メールの送信
    print("ok.")

def gmail6():
    # 以下にGmailの設定を書き込む★ --- (*1)
    gmail_account = "atsuri.snoopy@gmail.com"
    gmail_password = "11FlowBack26"
    # メールの送信先★ --- (*2)
    mail_to = "atsuri.snoopy@gmail.com"
    
    # メールデータ(MIME)の作成 --- (*3)
    subject = "パソコンの温度が高いです"
    body = "パソコンを休ませましょう。画面を暗くしましょう。"
    msg = MIMEText(body, "html")
    msg["Subject"] = subject
    msg["To"] = mail_to
    msg["From"] = gmail_account

    # Gmailに接続 --- (*4)
    server = smtplib.SMTP_SSL("smtp.gmail.com", 465,
        context=ssl.create_default_context())
    server.login(gmail_account, gmail_password)
    server.send_message(msg) # メールの送信
    print("ok.")

def gmail7():
    # 以下にGmailの設定を書き込む★ --- (*1)
    gmail_account = "atsuri.snoopy@gmail.com"
    gmail_password = "11FlowBack26"
    # メールの送信先★ --- (*2)
    mail_to = "atsuri.snoopy@gmail.com"
    
    # メールデータ(MIME)の作成 --- (*3)
    subject = "パソコンの温度が高いです"
    body = "アプリケーションなど使用していないものを消しましょう。充電が50%未満なので、充電しましょう。画面も暗くしましょう。"
    msg = MIMEText(body, "html")
    msg["Subject"] = subject
    msg["To"] = mail_to
    msg["From"] = gmail_account

    # Gmailに接続 --- (*4)
    server = smtplib.SMTP_SSL("smtp.gmail.com", 465,
        context=ssl.create_default_context())
    server.login(gmail_account, gmail_password)
    server.send_message(msg) # メールの送信
    print("ok.")

def gmail8():
    # 以下にGmailの設定を書き込む★ --- (*1)
    gmail_account = "atsuri.snoopy@gmail.com"
    gmail_password = "11FlowBack26"
    # メールの送信先★ --- (*2)
    mail_to = "atsuri.snoopy@gmail.com"
    
    # メールデータ(MIME)の作成 --- (*3)
    subject = "パソコンの温度が高いです"
    body = "アプリケーションなど使用していないものを消しましょう。画面を暗くしましょう。"
    msg = MIMEText(body, "html")
    msg["Subject"] = subject
    msg["To"] = mail_to
    msg["From"] = gmail_account

    # Gmailに接続 --- (*4)
    server = smtplib.SMTP_SSL("smtp.gmail.com", 465,
        context=ssl.create_default_context())
    server.login(gmail_account, gmail_password)
    server.send_message(msg) # メールの送信
    print("ok.")
