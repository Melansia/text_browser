from collections import deque
import os
import sys
import requests
from bs4 import BeautifulSoup
from colorama import Fore


def back(pages_stack, history):
    try:
        page = pages_stack.popleft()
        with open(history[page]) as file:
            print(file.read())
    except IndexError:
        return


def compose_url(url):
    return url if "https://" in url else f"https://{url}"


def create_directory(directory_path=f"{os.getcwd()}"):
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)


def write_file(path, file_content):
    with open(path, 'w', encoding='UTF-8') as file:
        file.write(file_content)


def get_content(r):
    soup = BeautifulSoup(r.content, 'html.parser')
    for link in soup.find_all('a'):
        link.string = ''.join([Fore.BLUE, link.get_text()])
    return soup.get_text()


def is_valid_url(url):
    return "." in url


def main():
    try:
        path = sys.argv[1]
    except IndexError:
        print("Not enough argument were passed")
        path = os.getcwd()

    create_directory(path)

    history = {}
    pages_stack = deque()

    while True:
        user_inp = input()

        if user_inp == "exit":
            break
        elif user_inp == "back":
            back(pages_stack, history)
            continue

        page_path = os.path.join(path, user_inp.split('.')[0] if "https://" not in user_inp else user_inp.lstrip("https://"))

        if os.path.exists(page_path):
            with open(page_path) as file:
                print(file.read())
                continue

        elif is_valid_url(user_inp):
            url = compose_url(user_inp)
            req = requests.get(url)
            if req:
                print(get_content(req))
                write_file(page_path, get_content(req))
                pages_stack.append(user_inp)
                history[user_inp] = page_path
        else:
            print("Invalid URL")


if __name__ == "__main__":
    main()