import random
import re

import nltk
import requests as requests
from bs4 import BeautifulSoup
from nltk import WordNetLemmatizer, tokenize


def classify_websites():
    lines = open("websites.txt", "r").read().splitlines()
    url = random.choice(lines)

    print(url)
    webpage = BeautifulSoup(requests.get(url).content, "html.parser")
    lemmatizer = WordNetLemmatizer()

    for result in webpage.find_all("p"):
        information = re.sub(r"\[\d+\]", "", result.text)

        print(information)
