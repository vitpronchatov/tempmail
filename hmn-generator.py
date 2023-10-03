import requests

url = 'https://hidemy.io/ua/demo/'

if 'Ваша електронна пошта' in requests.get(url).text:
    
    email = input('Введіть електронну пошту для отримання тестового періода: ')

    response = requests.post('https://hidemy.io/ua/demo/success/', data={
        "demo_mail": f"{email}"
    })

    if 'Ваш код вислано на пошту' in response.text:
        print('Пошта підтверджена. Код відправлений на вашу пошту!')
    else:
        print('Вказана пошта не підходить для отримання тестового періода ')

else:
    print('Неможливо отримати тестовий період')
