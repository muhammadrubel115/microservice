import requests

access_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzY2Njc4NTU3LCJpYXQiOjE3NjY2Nzc2NTcsImp0aSI6IjY1NmQwOWJiZDI4ZTQ0NjY4MGRmZjFhOGJmZTc1ZWU4IiwidXNlcl9pZCI6IjgiLCJ1c2VyX3V1aWQiOiJmYTY2ZWY5OC04MWM2LTRkYWEtOTViNy1kMTQyNWQ0YzBkM2QiLCJyb2xlIjoidXNlciIsInRva2VuX3ZlcnNpb24iOjEsImlzX2FjdGl2ZSI6dHJ1ZX0.E0IgZDCwQ0pXaKOWA4X3ELY2G7dJ6j9P7V4KdX3biWQ"

headers = {
    "Authorization": f"Bearer {access_token}"
}

response = requests.get("http://localhost:8000/profile/", headers=headers)

if response.status_code == 200:
    print("Profile data:")
    print(response.json())
else:
    print(f"Failed to get profile: {response.status_code}")
    print(response.json())
