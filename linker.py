import os
import requests
from colorama import Fore
import json
import threading
from datetime import datetime

lock = threading.Lock()

def linkpromo(promo):
    inputTokens = "Input/tokens.txt"
    outputFolder = "Output"
    outputTokens = os.path.join(outputFolder, "tokens.txt")
    outputPromos = os.path.join(outputFolder, "promos.txt")
    outputCombined = os.path.join(outputFolder, "combined.txt")
    outputUsedPromos = os.path.join(outputFolder, "usedpromos.txt")

    def fileExithm(file_path):
        if not os.path.exists(file_path):
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            open(file_path, 'w').close()

    def loadLines(file_path):
        if os.path.exists(file_path):
            with open(file_path, 'r') as file:
                return [line.strip() for line in file.readlines() if line.strip()]
        return []

    def update_file(file_path, lines):
        with open(file_path, 'w') as file:
            file.writelines(line + '\n' for line in lines)

    def writeFile(file_path, content):
        fileExithm(file_path)
        with open(file_path, 'a') as file:
            file.write(content + '\n')

    def time_right_now():
        return datetime.now().strftime("%I:%M %p")

    fileExithm(outputTokens)
    fileExithm(outputPromos)
    fileExithm(outputCombined)
    fileExithm(outputUsedPromos)

    with lock:
        tokens = loadLines(inputTokens)
        if not tokens:
            print(f"{Fore.LIGHTRED_EX}No tokens available in {inputTokens}.{Fore.RESET}")
            return
        token_line = tokens.pop(0)
        update_file(inputTokens, tokens)

    token = token_line.split(":")[-1]

    try:
        promo_id, promo_jwt = promo.split('/')[5:7]
        promo_url = f"https://discord.com/api/v9/entitlements/partner-promotions/{promo_id}"
        headers = {
            "authorization": token,
            'accept': '*/*',
            'accept-language': 'en-US,en;q=0.9',
            'content-type': 'application/json',
            'origin': 'https://discord.com',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
        }

        response = requests.post(promo_url, headers=headers, json={"jwt": promo_jwt})

        if response.status_code == 200:
            promo_data = response.json()
            promo_redemption_id = promo_data.get("code")

            if promo_redemption_id:
                print(f"{Fore.LIGHTWHITE_EX}{time_right_now()} | {Fore.RESET}{Fore.LIGHTCYAN_EX}PROMO{Fore.RESET} | LINKED {Fore.LIGHTWHITE_EX}[Code: {Fore.RESET}{Fore.LIGHTBLUE_EX}{promo_redemption_id}{Fore.RESET}{Fore.LIGHTWHITE_EX}]")
                writeFile(outputPromos, f"https://promos.discord.gg/{promo_redemption_id}")
                writeFile(outputTokens, token_line)
                writeFile(outputCombined, f"{token_line}|https://promos.discord.gg/{promo_redemption_id}")
                writeFile(outputUsedPromos, promo)
        else:
            print(f"{Fore.LIGHTWHITE_EX}{time_right_now()} | {Fore.RESET}{Fore.LIGHTRED_EX}ERROR{Fore.RESET} | Failed to retrieve promo {Fore.LIGHTWHITE_EX}[Error: {Fore.RESET}{Fore.LIGHTRED_EX}{response.text}{Fore.RESET}{Fore.LIGHTWHITE_EX}]{Fore.RESET}")

    except Exception as e:
        print(f"{Fore.LIGHTWHITE_EX}{time_right_now()} | {Fore.RESET}{Fore.LIGHTRED_EX}ERROR{Fore.RESET} | Exception {Fore.LIGHTWHITE_EX}[Error: {Fore.RESET}{Fore.LIGHTRED_EX}{str(e)}{Fore.RESET}{Fore.LIGHTWHITE_EX}]{Fore.RESET}")
