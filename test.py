import requests


url = './github.png'
with open(url, 'rb') as image:
  f = image.read()
  b = str(bytearray(f))

  
response = requests.post(
  url="63.35.31.27:8000/admin",
  json={
    "wantedId": 16,
    "name": "깃허브",
    "sex": True,
    "age": 60,
    "wantedType": True,
    "height": 182,
    "weight": "건장한 체격",
    "registeredAddress": "인천 서구",
    "residence": "인천 서구",
    "criminal": "사람 빡치게 함",
    "characteristic": "머지 충돌을 계속 냄",
    "image": b
  }                         
)

if response.status_code == 201:
  print("request succed")
else:
  print(response)