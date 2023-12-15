import requests

response = requests.post(url='http://127.0.0.1:5000/user',
                         json={'name': 'roman3',
                               'password': 'password',
                               'e_mail': '1jhgj@hghjg.ru'})
print(response.status_code)
print(response.text)

# response = requests.get(url='http://127.0.0.1:5000/adv/1')
# print(response.status_code)
# print(response.text)
# #
# #
response = requests.get(url='http://127.0.0.1:5000/user/1')
print(response.status_code)
print(response.text)


response = requests.post(url='http://127.0.0.1:5000/adv',
                         json={'header': 'HEADER',
                               'description': 'DESCRIPTION',
                               'author': 1
                               },
                         )
print(response.status_code)
print(response.text)

# response = requests.patch(url='http://127.0.0.1:5000/user/4',
#                           json={'e_mail': '1135552'},
#                          )
# print(response.status_code)
# print(response.text)
#
#



# response = requests.delete(url='http://127.0.0.1:5000/user/4',
#                          )
# print(response.status_code)
# print(response.text)


# response = requests.patch(url='http://127.0.0.1:5000/adv/2',
#                          json={'id': 1,
#                                'description': 'Новое описание'},
#                          )
# print(response.status_code)
# print(response.text)
#
#
# response = requests.post(url='http://127.0.0.1:5000/user',
#
#                          json={'name': '1134412'},
#                          )
# print(response.status_code)
# print(response.text)


# response = requests.get(url='http://127.0.0.1:5000/user/4',
#                          )
# print(response.status_code)
# print(response.text)
