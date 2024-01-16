import requests

data = {
    'sepal_length': 1.5,
    'sepal_width': 2.5,
    'petal_length': 2.5,
    'petal_width': 2.5,
    'iris_class': 3
}
headers = {'Content-Type' : 'application/json'}
response = requests.post('http://127.0.0.1:5000/api/data', json=data, headers=headers)
print(response)
print(response.json())
print(response.status_code)
print(response.headers)

#GET ALL TEST
# response = requests.get("http://127.0.0.1:5000/api/data")
# print(response)
# print(response.json())
# print(response.headers)




#DELETING TEST
# response = requests.delete("http://127.0.0.1:5000/api/data/9")
# print(response)
# print(response.json())
# print(response.headers)



