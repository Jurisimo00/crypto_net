import json
import os
from pathlib        import Path
from .coin          import Coin

ufile_path = "./users.json"

def load_users():
    with open(ufile_path, "r") as f:
        data = f.read()
        return json.loads(data)

def write_back(users):
    path = Path(ufile_path)
    if path.exists():
        os.remove(ufile_path)
    with open(ufile_path, "w") as f:
        f.write(json.dumps(users))

def find_user(username, users):
    for u in users:
        if u["username"] == username:
            return u
    return None

def find_user_by_ip(ip):
    users = load_users()
    for u in users:
        if u["ip"] == ip:
            return u
    return None

def add_crypto_to_user(username, coin: Coin):
    def find_coin_in_user(user, coin_symbol):
        for c in user["wallet"]:
            if c["symbol"] == coin_symbol:
                return c
        return None

    users = load_users()
    user = find_user(username, users)
    coin = find_coin_in_user(user, coin.symbol)         
    if coin is not None:
        coin["balance"] += coin.balance
    else:
        user["wallet"].append(coin.as_dict())
    write_back(users)

def delete_sessions_with_same_ip(ip):
    users = load_users()
    for u in users:
        if u["ip"] == ip:
            u["ip"] = ""
    write_back(users)

def update_user(user, coin: Coin, dollar_amount):
    users = load_users()
    for u in users:
        if u["username"] == user["username"]:
            u["dollar_balance"] += dollar_amount
            for c in u["wallet"]:
                if c["symbol"] == coin.symbol:
                    c["balance"] += coin.balance
                    write_back(users)
                    return
            u["wallet"].append(coin.as_dict())
            write_back(users)

def authenticate_user(username, pwd, ip) -> bool:
    users = load_users()
    user = find_user(username, users)
    if user is not None:
        if user["pwd"] == pwd:
            user["ip"] = ip
            write_back(users)
            return True
    return False

def logout_user(ip) -> bool:
    users = load_users()
    found = False
    for u in users:
        if u["ip"] == ip:
            found = True
            u["ip"] = ""
    write_back(users)
    return found

