import random
import re

import nltk
import requests as requests
from bs4 import BeautifulSoup
from nltk import WordNetLemmatizer, tokenize


def register_topic(topic):
    topic += "\n"
    with open(f"meta/topics.txt", 'a+') as file:
        file.seek(0)
        if topic in file.readlines():
            return
        file.write(topic)


def log_info(topic, info):
    with open(f"info/{topic}.site", 'a+') as file:
        file.seek(0)
        if info in file.readlines():
            return
        try:
            file.write(f"{info}\n")
            register_topic(topic)
        except UnicodeEncodeError:
            return


def scrape_info():
    lines = open("meta/websites.txt", "r").read().splitlines()
    url = random.choice(lines)

    webpage = BeautifulSoup(requests.get(url).content, "html.parser")
    lemmatizer = WordNetLemmatizer()

    for result in webpage.find_all("p"):
        information = re.sub(r"\[\d+\]", "", result.text)

        words = tokenize.word_tokenize(information)
        words = [lemmatizer.lemmatize(word) for word in words]
        tags = nltk.pos_tag(words)
        tree = nltk.ne_chunk(tags, binary=True)

        keywords = list(
            " ".join(i[0] for i in t) for t in tree if hasattr(t, "label") and t.label() == "NE"
        )

        for topic in keywords:
            print(topic)
            log_info(topic, information)


def is_valid_link(link):
    if link.find("http") != -1:
        return False
    if link.find("/wiki/") != 0:
        return False
    if link.find(":") != -1:
        return False
    if link.find("#") != -1:
        return False
    if link.find(".") == -1:
        return False

    return True


def log_site(site):
    site += '\n'

    with open("meta/websites.txt", 'a+') as file:
        file.seek(0)
        if site in file.readlines():
            return
        try:
            file.write(site)
            print(site)
        except UnicodeEncodeError:
            return


def search_sites():
    lines = open("meta/websites.txt", "r").read().splitlines()
    url = random.choice(lines)

    webpage = BeautifulSoup(requests.get(url).text, "html.parser")

    for link in webpage.find_all('a'):
        link = str(link.get('href'))
        print(link)

        if is_valid_link(link):
            log_site(f"https://en.wikipedia.org{link}")
