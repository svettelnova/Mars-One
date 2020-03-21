from requests import get, post, delete

print(get('http://localhost:5000/api/jobs').json())
print(get('http://localhost:5000/api/jobs/1').json())
print(get('http://localhost:5000/api/jobs/999').json())
try:
    print(get('http://localhost:5000/api/jobs/abc').json())
except:
    print("Error on getting job with id='abc'")
try:
    print(post('http://localhost:5000/api/jobs',
               json={'team_leader_id': 1,
                     'description': 'search for water below the surface',
                     'work_size': 12,
                     'is_finished': True}).json())
except:
    print("Post failed")
try:
    # В request не будет json
    print(post('http://localhost:5000/api/jobs',
               json1={'team_leader_id': 1,
                      'description': 'search for water below the surface',
                      'work_size': 12,
                      'is_finished': True}).json())
except:
    print("Post failed")
try:
    # Нет work_size, выдаст Bad request
    print(post('http://localhost:5000/api/jobs',
               json={'team_leader_id': 1,
                     'description': 'search for water below the surface',
                     'is_finished': True}).json())
except:
    print("Post failed")
try:
    # Work_size задан строкой
    print(post('http://localhost:5000/api/jobs',
               json={'team_leader_id': 1,
                     'description': 'search for water below the surface',
                     'work_size': "12",
                     'is_finished': True}).json())
except:
    print("Post failed")
try:
    print(delete('http://localhost:5000/api/jobs/1').json())
except:
    print('Delete failed')
try:
    print(delete('http://localhost:5000/api/jobs/3').json())
except:
    print('Delete failed')
try:
    # Не выбран id
    print(delete('http://localhost:5000/api/jobs').json())
except:
    print('Delete failed')
try:
    # Нет работы с id = 999 нет в базе
    print(delete('http://localhost:5000/api/jobs/999').json())
except:
    print('Delete failed')
