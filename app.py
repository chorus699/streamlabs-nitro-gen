import json, tls_client, time, requests, re, threading, random
from console import Console
import os
import pickle
import time
import random
import re
import requests
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from urllib.parse import unquote
from bs4 import BeautifulSoup
from linker import linkpromo

console = Console()
with open('config.json', 'r') as config_file: config = json.load(config_file)
license_key = config.get("license")
api_host = "http://127.0.0.1:5000"


class tempmail:
    EMAIL_DOMAIN = "gmail.com"
    def __init__(self, client_secret_file='client_secret.json', token_file='token.json'):
        self.client_secret_file = client_secret_file
        self.token_file = token_file
    def authenticate_gmail(self):
        creds = None
        if os.path.exists(self.token_file):
            with open(self.token_file, 'rb') as token:
                creds = pickle.load(token)
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(self.client_secret_file, SCOPES)
                creds = flow.run_local_server(port=0)
            with open(self.token_file, 'wb') as token:
                pickle.dump(creds, token)
        return creds
    def create_temp_email(self):
        random_string = ''.join(random.choices('abcdefghijklmnopqrstuvwxyz0123456789', k=5))
        temp_email = f"streamlabschorus+{random_string}@{self.EMAIL_DOMAIN}"
        return temp_email
    def get_email_code(self, generated_email, max_attempts=20, retry_interval=5):
        attempts = 0
        while attempts < max_attempts:
            try:
                time.sleep(5)
                creds = self.authenticate_gmail()
                service = build('gmail', 'v1', credentials=creds)
                unread_msgs = service.users().messages().list(userId='me', labelIds=['INBOX', 'UNREAD']).execute()
                messages = unread_msgs.get('messages', [])
                for msg in messages:
                    msg_id = msg['id']
                    message = service.users().messages().get(userId='me', id=msg_id).execute()
                    subject = next((header['value'] for header in message['payload']['headers'] if header['name'] == 'Subject'), None)
                    to_address = next((header['value'] for header in message['payload']['headers'] if header['name'] == 'To'), None)
                    if to_address == generated_email:
                        otp_match = re.search(r'\d{8}', subject)
                        if otp_match:
                            service.users().messages().modify(userId='me', id=msg_id, body={'removeLabelIds': ['UNREAD']}).execute()
                            return otp_match.group(0)
                attempts += 1
                time.sleep(retry_interval)
            except Exception as e:
                print(f"Error while fetching OTP from Gmail: {e}")
        raise Exception("Failed to retrieve verification code from Gmail")

def puller(cookies):
    try:
        
        with open('cookies.txt', 'a') as f:
            f.write(f"{cookies}\n")
        
        url = f"https://publisher.scrappey.com/api/v1?key=wceC2WN0xos5Fbqj4fqSMliQo4au3cOMKKJZYMk0bkIy9ARV9itNDoN3LKfz"
        json_data = {
            'cmd': 'request.get',
            'url': 'https://streamlabs.com/discord/nitro',
            'browser': [{'name': 'chrome'}],
            'noDriver': True,
            'cookies': cookies,
        }

        response = requests.post(url, json=json_data)
        if response.status_code == 200:
            data = response.json()
            redirect_url = data['solution']['currentUrl']
            print(redirect_url)
            return redirect_url
        else:
            print("Error with the request:", response.status_code)
            return None
    except Exception as e:
        print("An error occurred:", e)
        return None

def twocaptchasolver():
    max_attempts = 50
    for attempt in range(max_attempts):
        try:
            if attempt > 0: console.info(f"Retrying in 1 minute... (Attempt {attempt}/{max_attempts})"); time.sleep(3)
            params = {"url": "https://streamlabs.com/slid/signup", "sitekey": "0x4AAAAAAACELUBpqiwktdQ9"}
            response = requests.get(f"{api_host}/turnstile", params=params, timeout=120)
            if response.status_code == 200:
                result = response.json()
                if result["status"] == "success": return result["result"]
                else: console.error(f"Turnstile-Solver failed: {result.get('error')}")
            else: console.error(f"Error from Turnstile-Solver: HTTP {response.status_code}")
        except requests.RequestException as e: console.error(f"Network error occurred: {str(e)}")
        except Exception as e: console.error(f"An unexpected error occurred: {str(e)}")
    console.error("Max attempts reached. Could not solve captcha.")
    return None

def get_twitter_token():
    try:
        with open('tokens.txt', 'r') as f: tokens = f.readlines()
        if not tokens: return None
        token = tokens[0].strip()
        with open('tokens.txt', 'w') as f: f.writelines(tokens[1:])
        return token
    except FileNotFoundError: console.error("tokens.txt file not found."); return None

proxy_url = "ADD YOUR PROXY "

def create_session_with_proxy():
    ses = tls_client.Session(client_identifier="chrome_131", random_tls_extension_order=True)
    ses.proxies = {'http': f'http://{proxy_url}', 'https': f'http://{proxy_url}'}
    return ses

def creator():
    ses = create_session_with_proxy()
    captcha_token = twocaptchasolver()
    if not captcha_token: console.error("Captcha solving failed."); return
    temp_mail_instance = tempmail()
    email = temp_mail_instance.create_temp_email()
    headers = {'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8', 'accept-language': 'en-US,en;q=0.5', 'cache-control': 'no-cache', 'pragma': 'no-cache', 'priority': 'u=0, i', 'sec-ch-ua': '"Brave";v="131", "Chromium";v="131", "Not_A Brand";v="24"', 'sec-ch-ua-mobile': '?0', 'sec-ch-ua-platform': '"Windows"', 'sec-fetch-dest': 'document', 'sec-fetch-mode': 'navigate', 'sec-fetch-site': 'none', 'sec-fetch-user': '?1', 'sec-gpc': '1', 'upgrade-insecure-requests': '1', 'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36'}
    ses.get('https://streamlabs.com/slid/signup', headers=headers)
    xsrf = ses.cookies.get('XSRF-TOKEN')
    if not xsrf: console.error("Failed to fetch XSRF token."); return
    ses.headers.update({'accept': 'application/json, text/plain, */*', 'cache-control': 'no-cache', 'client-id': '419049641753968640', 'content-type': 'application/json', 'origin': 'https://streamlabs.com', 'referer': 'https://streamlabs.com/', 'x-xsrf-token': xsrf})
    json_data = {'email': email, 'username': '', 'password': 'Jignewah382ry83#', 'agree': True, 'agreePromotional': False, 'dob': '', 'captcha_token': captcha_token, 'locale': 'en-US'}
    response = ses.post('https://api-id.streamlabs.com/v1/auth/register', json=json_data)
    if response.status_code != 200: console.error("Registration failed."); return
    otp_verified = False
    while not otp_verified:
        otp = temp_mail_instance.get_email_code(email)
        if otp:
            otp_verified = verifier(xsrf, otp, email, ses)
            if otp_verified:
                console.info(f"Verified -> {email}")
                csrf_token = csrf(xsrf, ses)
                twitter_token = get_twitter_token()
                if twitter_token:
                    success = merge(ses, csrf_token, twitter_token)
                    if success:
                        console.success("Twitter account successfully linked!")
                        cookies = ses.cookies
                        formatted_cookies = "; ".join([f"{cookie.name}={cookie.value}" for cookie in cookies])
                        promo = puller(formatted_cookies)
                        if promo:
                            console.promo(f"Promo -> {promo}")
                            linkpromo(promo)
                        else: console.error("Failed to retrieve promo URL.")
                    else: console.error("Failed to link Twitter account.")
        break

def verifier(xsrf, otp, email, ses):
    url = "https://api-id.streamlabs.com/v1/users/@me/email/verification/confirm"
    payload = {"code": otp, "email": email, "tfa_code": ""}
    ses.headers.update({"x-xsrf-token": xsrf})
    response = ses.post(url, json=payload)
    if response.status_code == 204:
        console.info(f"Verification Successful for: {email}")
        return True
    else:
        console.error("Verification Failed:", response.text)
        return False

def csrf(xsrf, ses):
    url = "https://api-id.streamlabs.com/v1/identity/clients/419049641753968640/oauth2"
    payload = {"origin": "https://streamlabs.com", "intent": "connect", "state": ""}
    headers = {"X-XSRF-Token": xsrf, "Content-Type": "application/json"}
    response = ses.post(url, json=payload, headers=headers)
    if response.status_code == 200:
        data = response.json()
        redirect_url = data.get("redirect_url")
        if redirect_url:
            while redirect_url:
                redirect_response = ses.get(redirect_url, allow_redirects=False)
                ses.cookies.update(redirect_response.cookies)
                if redirect_response.status_code in (301, 302) and 'Location' in redirect_response.headers:
                    redirect_url = redirect_response.headers['Location']
                else:
                    match = re.search(r"var\s+redirectUrl\s*=\s*'(.*?)';", redirect_response.text)
                    if match:
                        redirect_url = match.group(1)
                        red4 = ses.get(redirect_url)
                        ses.cookies.update(red4.cookies)
                        red5 = ses.get("https://streamlabs.com/dashboard")
                        ses.cookies.update(red5.cookies)
                        soup = BeautifulSoup(red5.text, "html.parser")
                        csrf = soup.find("meta", {"name": "csrf-token"})["content"]
                        return csrf
        else: console.error("Redirect URL not found."); return None
    else: console.error(f"Request failed: {response.status_code} - {response.text}"); return None

def merge(ses, csrf, twitter_token: str) -> bool:
    max_retries = 5
    retries = 0
    while retries < max_retries:
        try:
            response = ses.get("https://streamlabs.com/api/v5/user/accounts/merge/twitter_account", params={"r": "/dashboard#/settings/account-settings/platforms"})
            if response.status_code != 200: console.error(f"Failed to get OAuth URL: {response.status_code}"); return False
            oauth_url = response.json().get('redirect_url')
            if not oauth_url: console.error("Failed to retrieve OAuth URL."); return False
            oauth_token = oauth_url.split("oauth_token=")[1]
            session = tls_client.Session('chrome_131', random_tls_extension_order=True)
            auth_response = session.get(oauth_url, headers={'cookie': f"auth_token={twitter_token};"})
            try:
                authenticity_token = auth_response.text.split(' <input name="authenticity_token" type="hidden" value="')[1].split('">')[0]
            except IndexError: console.error("Invalid Twitter Account."); return False
            auth_data = {'authenticity_token': authenticity_token, 'oauth_token': oauth_token}
            final_response = session.post('https://twitter.com/oauth/authorize', data=auth_data, headers={'cookie': f"auth_token={twitter_token};"})
            try:
                redirect_url = final_response.text.split('<p>If your browser doesn\'t redirect you please <a class="maintain-context" href="')[1].split('">')[0]
                if redirect_url:
                    if 'You are being' in redirect_url: console.error("Twitter account already used."); return False
                    session.headers.update({'referer': "https://twitter.com"})
                    response = ses.get(unquote(redirect_url).replace("amp;", '').replace("amp;", ''))
                    if response.status_code == 302: return True
                    else: console.error(f"Failed to link Twitter account: {response.status_code}")
                else: console.error("Failed to find redirect URL."); retries += 1; time.sleep(2); continue
            except IndexError: retries += 1; time.sleep(2); continue
        except Exception as e: console.error(f"Failed to link Twitter account: {e}"); retries += 1; time.sleep(2); continue
    console.error("Exceeded maximum retries. Failed to link Twitter account."); return False

def loop_creator(): 
    while True: creator()

threads = []
thread_count = config.get("num_threads", 3)
for i in range(thread_count): thread = threading.Thread(target=loop_creator, name=f"Thread-{i+1}", daemon=True); threads.append(thread); thread.start()

try: 
    while True: time.sleep(1)
except KeyboardInterrupt: console.error("Exiting program.")
