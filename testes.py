import requests

headers = {
    'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI2IiwiZXhwIjoxNzkzNzUyNDcxfQ.EN4A1BYdhR9dgiM7H5gwPMkdNrhEBHQUXmm67mFz7Ro'
}

requisicao = requests.get('http://127.0.0.1:8000/auth/refresh', headers=headers)

print(requisicao)
print(requisicao.json())