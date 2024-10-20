import sys
import math
import threading
import time
import random
from durakonline import durakonline
from datetime import datetime

FILE_DIRECTORY: str = "./accounts.txt"
DEBUG_MODE: bool = False

class DurakOnlineTools:

    tokens: [str] = []
    accounts: [durakonline.Client] = []

    def init(self) -> None:
        self.log(f"Load {self.load_accounts()} accounts", "CONSOLE")
        self.authorization_accounts()

    def generate_tokens(self, length: int, count: int) -> [str]:
        tokens = []
        characters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789./"
        for _ in range(count):
            token = "$2a$06$" + ''.join(random.choice(characters) for _ in range(length))
            print(token)
            tokens.append(token)
        return tokens

    def load_accounts(self) -> int:
        """
        data accounts in file by format:
            "
            token
            token
            ...
            "
        """
        with open(FILE_DIRECTORY, 'r') as file:
            self.tokens = file.read().split()
        return len(self.tokens)

    def done(self) -> None:
        self.log("Done\n", "CONSOLE")
        self.pages[0]()

    def authorization_accounts(self) -> None:
        self.log("Authorizations accounts::", "CONSOLE")
        with open(FILE_DIRECTORY, 'a') as file:
            for token in self.tokens:
                try:
                    account = durakonline.Client(token=token, debug=DEBUG_MODE)
                    file.write(f"{token}\n")
                except Exception as e:
                    self.log("Failed log account", token)
                    if not REMOVE_INVALID_ACCOUNTS:
                        file.write(f"{token}\n")
                    continue
                self.accounts.append(account)
                self.log("Logged in", account.uid)
                time.sleep(.1)
        self.log("All auth", "CONSOLE")

    def log(self, message: str, server: str) -> None:
        print(f">> [{server}] [{datetime.now().strftime('%H:%M:%S')}] {message}")

if __name__ == "__main__":
    tools = DurakOnlineTools()
    count = int(input("Введите количество токенов: "))
    tokens = tools.generate_tokens(length=22, count=count)
    with open(FILE_DIRECTORY, 'a') as file:
        for token in tokens:
            file.write(f"{token}\n")
    tools.init()