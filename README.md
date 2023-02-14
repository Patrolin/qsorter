# setup
Install python youtube api from https://developers.google.com/youtube/v3/quickstart/python

Create google project at https://console.cloud.google.com (must be under an organization, otherwise it will have 0 max quota for no reason)

Create api key, Edit api key > Set restricted

Create OAUTH client id > Create OATH consent screen

Create OAUTH client id > Download JSON > Save to client_secret.json

Search "All quotas" at https://console.cloud.google.com to confirm you have a nonzero max quota (requests will return a 403)
