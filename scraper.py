import random
import re

import nltk
import requests as requests
from bs4 import BeautifulSoup
from nltk import WordNetLemmatizer, tokenize


def register_topic(topic):
    topic += "\n"
    with open(f"topics.txt", 'a+') as file:
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


def classify_websites():
    lines = open("websites.txt", "r").read().splitlines()
    url = random.choice(lines)

    print(url)
    webpage = BeautifulSoup(requests.get(url).content, "html.parser")
    lemmatizer = WordNetLemmatizer()

    for result in webpage.find_all("p"):
        information = re.sub(r"\[\d+\]", "", result.text)

        print(information)

        words = tokenize.word_tokenize(information)
        words = [lemmatizer.lemmatize(word) for word in words]
        tags = nltk.pos_tag(words)
        tree = nltk.ne_chunk(tags, binary=True)

        keywords = list(
            " ".join(i[0] for i in t) for t in tree if hasattr(t, "label") and t.label() == "NE"
        )

        for topic in keywords:
            log_info(topic, information)
            print(topic)
