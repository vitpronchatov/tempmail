import requests
import json
import time


class Mail:

    def __init__(self, m=None):

        """Процедура инициализации"""

        a = "https://www.1secmail.com/api/v1/?action=genRandomMailbox&count=1"
        if m is None:
            self.mail = json.loads(requests.post(a).text)[0]
        else:
            self.mail = m
        print(self.mail)

    def check_messages(self):

        """Процедура проверки входящего сообщения"""

        a = self.mail.split('@')
        b = json.loads(
            requests.get(f"https://www.1secmail.com/api/v1/?action=getMessages&login={a[0]}&domain={a[1]}").text)
        lis = []
        for i in b:
            lis.append('|Id: ' + str(i["id"]) + "\n" + "|From: " + i["from"] + "\n" + "|Subject: " + i[
                "subject"] + "\n" + "|Date: " + i["date"])
        return "\n\n".join(lis)

    def get_message_id(self):

        """Получение идентификатора сообщения"""

        a = self.mail.split('@')
        b = json.loads(
            requests.get(f"https://www.1secmail.com/api/v1/?action=getMessages&login={a[0]}&domain={a[1]}").text)
        try:
            return b[0]['id']
        except:
            print("No messages!")

    def get_message_subject(self):

        """Получение заголовка сообщения"""

        a = self.mail.split('@')
        b = json.loads(
            requests.get(f"https://www.1secmail.com/api/v1/?action=getMessages&login={a[0]}&domain={a[1]}").text)
        try:
            return b[0]['subject']
        except:
            print("No messages!")

    def get_message_by_id(self, id):

        """Процедура открытия конкретного сообщения (по айди)"""

        b = self.mail.split('@')
        d = json.loads(requests.get(
            f"https://www.1secmail.com/api/v1/?action=readMessage&login={b[0]}&domain={b[1]}&id={id}").text)
        html = d["htmlBody"]
        body = d["body"]
        if len(html) > 0:
            html = d["htmlBody"]
        else:
            html = "None"
        attach = d["attachments"]
        if len(attach) > 0:
            lis = []
            attach = d["attachments"]
            for i in attach:
                lis.append(
                    f'https://www.1secmail.com/api/v1/?action=download&login={b[0]}&domain={b[1]}&id={id}&file={i["filename"]}')
            attach = ", ".join(lis)
        else:
            attach = "None"
        c = '|Id: ' + str(d["id"]) + "\n" + "|From: " + d["from"] + "\n" + "|Subject: " + d[
            "subject"] + "\n" + "|Date: " + d["date"] + "\n" + "|Body: " + body + "\n|TextBody: " + d[
                "textBody"] + "\n" + "|HtmlBody: " + html + "\n" + "|Attachments: " + attach
        return c

    def get_message_email_name(self):
        return self.mail


def check_email(email_name):
    response = requests.post('https://hidemy.io/ru/demo/success/', data={
        "demo_mail": f"{email_name}"})

    if 'Ваш код выслан на почту' in response.text:
        email_is_valid = True
        print("Указанная почта подходит для получения тестового периода!")
        return email_is_valid
    else:
        email_is_valid = False
        print('Указанная почта не подходит для получения тестового периода!')
        return email_is_valid


# Основной алгоритм получения кодов hidemy.name
url = 'https://hidemy.io/ru/demo/'

if 'Ваша электронная почта' in requests.get(url).text:
    email = Mail()
    email_name = email.get_message_email_name()

    email_is_valid = check_email(email_name)

    while email_is_valid is not True:
        email = Mail()
        email_name = email.get_message_email_name()
        email_is_valid = check_email(email_name)

    if email_is_valid:
        print("Ждем 70 секунд...")
        time.sleep(70)
        try:
            message = email.get_message_by_id(email.get_message_id())
            message_subject = email.get_message_subject()
        except:
            print("Ждем еще 20 секунд...")
            time.sleep(20)
            message = email.get_message_by_id(email.get_message_id())
            message_subject = email.get_message_subject()
        if message_subject == "Подтвердите e-mail":
            ver_link = message[message.find('Подтвердить') + 262:message.find('Подтвердить') + 306]
        print("Ссылка для подтверждения e-mail: ")
        print(ver_link)

        while True:
            try:
                response = requests.get(ver_link)
                if 'Спасибо' in response.text:
                    print('Почта подтверждена. Код отправлен на вашу почту!')
                    break
                else:
                    ver_link = input('Ссылка невалидная, повторите попытку: ')
            except:
                ver_link = input('Ссылка невалидная, повторите попытку: ')
                continue
            input("Нажмите Enter для продолжения...")

    print("Получение тестового кода...")
    time.sleep(10)

    message = email.get_message_by_id(email.get_message_id())
    print("Ваш тестовый код:")
    print(message[message.find('Ваш тестовый код: ') + 18:message.find('Ваш тестовый код: ') + 32])

    file = open("/content/drive/MyDrive/Colab Notebooks/codes.txt", 'a+')
    file.write('\n')
    file.write(message[message.find('Ваш тестовый код: ') + 18:message.find('Ваш тестовый код: ') + 32])
    lines = 0
    for line in file:
        lines += 1
    print('Сгенерировано кодов: ' + str(lines))
    file.close()
else:
    print('Невозможно получить тестовый период')