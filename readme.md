## Steps

1. [Create a User](https://botpress.com/reference/createuser-1)

run
```python
headers = {"Content-Type": "application/json", "Custom-Header": "value"}
body = {"name": "NAME", "id": "SOME_RANDOM_ID"}

response = requests.post(
    "https://chat.botpress.cloud/<CHAT_API_ID>/users", json=body, headers=headers
    )
```
to create a user key. The response will look like:

```
Success: {'user': {'id': 'SOME_RANDOM_ID', 'createdAt': '2025-05-08T21:06:56.806Z', 'updatedAt': '2025-05-08T21:06:56.806Z', 'name': 'NAME'}, 'key': 'USER_KEY'}
```

