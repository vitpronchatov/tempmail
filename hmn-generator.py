import requests

url = 'https://hidemy.io/ua/demo/'

if 'Ваша електронна пошта' in requests.get(url).text:
    
    email = input('Введіть електронну пошту для отримання тестового періода: ')

    response = requests.post('https://hidemy.io/ua/demo/success/', data={
        "demo_mail": f"{email}"
    })

    print(response.text)

    #if 'Ваш код вже відправлено на вказану електронну пошту' in response.text:
    #    confirm = input('Введіть отримане посилання для підтвердження e-mail адреси: ')
        
    #   while True:
    #        try:
    #            response = requests.get(confirm)
    #            if 'Дякую' in response.text:
    #                print('Пошта підтверджена. Код відправлений на вашу пошту!')
    #                break
    #            else:
    #                confirm = input('Посилання недійсне, повторіть спробу: ')
    #        except:
    #            confirm = input('Посилання недійсне, повторіть спробу: ')
    #            continue


    else:
        print('Вказана пошта не підходить для отримання тестового періода ')

else:
    print('Неможливо отримати тестовий період')
