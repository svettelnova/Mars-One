from requests import get, post, delete

try:
    print(get('http://localhost:5000/api/v2/users').json())
except:
    print('Get failed')
try:
    print(get('http://localhost:5000/api/v2/users/2').json())
except:
    print('Get failed')
# Неправильно задан адрес
try:
    print(get('http://localhost:5000/api/v2/user').json())
except:
    print('Get failed')
# В request не будет json
try:
    print(get('http://localhost:5000/api/v2/user').json1())
except:
    print('Get failed')
try:
    print(post('http://localhost:5000/api/v2/users', data={
        'surname': "Potter",
        'name': 'Harry',
        'age': 17,
        'position': 'crew member',
        'speciality': 'wizard',
        'address': 2,
        'email': 'theboywholived@mars.org',
        'hashed_password': 'Potter1980'
    }).json())
except:
    print('Post failed')
try:
    print(post('http://localhost:5000/api/v2/users', data={
        'surname': "Weasley",
        'name': 'Ron',
        'age': 17,
        'position': 'crew member',
        'speciality': 'wizard',
        'address': 2,
        'email': 'friendofHarryPotter@mars.org',
        'hashed_password': 'Weasley1980'
    }).json())
except:
    print('Post failed')
# Нет обязательных аргументов
try:
    print(post('http://localhost:5000/api/v2/users', data={
        'surname': "Granger",
        'name': 'Hermione',
        'age': 17,
        'position': 'crew member',
        'speciality': 'wizard',
        'email': '@mars.org'
    }).json())
except:
    print('Post failed')
try:
    print(delete('http://localhost:5000/api/v2/users/3').json())
except:
    print('Delete failed')
try:
    print(delete('http://localhost:5000/api/v2/users/2').json())
except:
    print('Delete failed')
# Не указан id пользователя
try:
    print(delete('http://localhost:5000/api/v2/users').json())
except:
    print('Delete failed')
# В json не будет request
try:
    print(delete('http://localhost:5000/api/v2/users/2').json1())
except:
    print('Delete failed')
