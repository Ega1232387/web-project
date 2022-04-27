from requests import get, post

print(post('http://localhost:5000/api/jobs',
           json={'id': 9, 'job': 'installation of radiation protection', 'team_leader': 1, 'work_size': 45,
                 'collaborators': '6, 4, 7', 'category': 1, 'is_finished': False}).json())  # id=9 exists
print(post('http://localhost:5000/api/jobs',
           json={'id': 10, 'job': 'installation of radiation protection'}).json())  # not full list of characters
print(post('http://localhost:5000/api/jobs').json())  # empty request
print(post('http://localhost:5000/api/jobs',
           json={'id': 12, 'job': 'searching green men', 'team_leader': 7, 'work_size': 35,
                 'collaborators': '4, 3, 8', 'category': 2, 'is_finished': False}).json())  # cool request
print(get('http://localhost:5000/api/jobs').json())
