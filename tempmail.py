import sys
import requests
import json
import time
import string
import random
from hashlib import md5
from TempMail import TempMail


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
    email = TempMail()
    inbox = TempMail.generateInbox(email)
    print(inbox.address)

    email_is_valid = check_email(inbox.address)

    while email_is_valid is not True:
        email = TempMail()
        inbox = TempMail.generateInbox(email)
        email_is_valid = check_email(inbox.address)

    print("Ждем 70 секунд...")
    time.sleep(70)
    message = TempMail.getEmails(email, inbox=inbox)
    print(message)

    # if email_is_valid:
    #     print("Ждем 70 секунд...")
    #     time.sleep(70)
    #     try:
    #         message = TempMail.getEmails(email, inbox=inbox)
    #         print(message)
    #      except:
    #          print("Ждем еще 20 секунд...")
    #          time.sleep(20)
    #          try:
    #              message = TempMail.getEmails(email, inbox=inbox)
    #              message_subject = email.get_message_subject()
    #          except:
    #              print("К сожалению получить письмо не получилось...")
    #              sys.exit()
    #     if message_subject == "Подтвердите e-mail":
    #         ver_link = message[message.find('Подтвердить') + 262:message.find('Подтвердить') + 306]
    #     else:
    #         print("Сообщение не получено...")
    #     print("Ссылка для подтверждения e-mail: ")
    #     print(ver_link)
    #
    #     while True:
    #         try:
    #             response = requests.get(ver_link)
    #             if 'Спасибо' in response.text:
    #                 print('Почта подтверждена. Код отправлен на вашу почту!')
    #                 break
    #             else:
    #                 ver_link = input('Ссылка невалидная, повторите попытку: ')
    #         except:
    #             ver_link = input('Ссылка невалидная, повторите попытку: ')
    #             continue
    #         input("Нажмите Enter для продолжения...")
    #
    # print("Получение тестового кода...")
    # time.sleep(10)
    #
    # message = email.get_message_by_id(email.get_message_id())
    # print("Ваш тестовый код:")
    # print(message[message.find('Ваш тестовый код: ') + 18:message.find('Ваш тестовый код: ') + 32])
    #
    # lines = 0
    # file = open("/content/drive/MyDrive/Colab Notebooks/codes.txt", 'a+')
    # file.write('\n')
    # file.write(message[message.find('Ваш тестовый код: ') + 18:message.find('Ваш тестовый код: ') + 32])
    # with open("/content/drive/MyDrive/Colab Notebooks/codes.txt") as file:
    #     for line in file:
    #         lines += 1
    #     print('Сгенерировано кодов: ' + str(lines))
    # file.close()
else:
    print('Невозможно получить тестовый период')