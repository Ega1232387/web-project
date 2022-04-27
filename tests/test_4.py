from requests import post, get

print(post('http://localhost:5000/api/jobs/10',
           json={'id': 10, 'job': 'installation of radiation protection'}).json())  # not full list of characters
print(post('http://localhost:5000/api/jobs/10').json())  # empty request
print(post('http://localhost:5000/api/jobs/10',
           json={'id': 10, 'job': 'installing a long-distance communication antenna', 'team_leader': 4, 'work_size': 23,
                 'collaborators': '6, 3, 8', 'category': 3, 'is_finished': True}).json())  # cool request
print(get('http://localhost:5000/api/jobs/10').json())