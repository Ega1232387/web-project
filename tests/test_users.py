from requests import get, post, delete

print(get('http://localhost:5000/api/users').json())
print(get('http://localhost:5000/api/users/7').json())
print(post('http://localhost:5000/api/users', json={
    'id': 8, 'name': 'Mike', 'surname': 'Smith', 'address': 'module_2',
    'email': 'smith@mars.org', 'age': 23, 'position': 'chief reseacher',
    'speciality': 'scientist', 'hashed_password': 'physics', 'modified_date': 'NULL'
}).json())
print(get('http://localhost:5000/api/users/8').json())
