# -*- coding: utf-8 -*-
import requests
import codecs
from bs4 import BeautifulSoup
import json

categorised_qs = {}
def write_one_game(url):
    """
    Writes one game to the file
    :param url: the url of the game we are writing (date format)
    :param file: the file we are writing to
    :return:
    """
    print('Fetching quiz for ' + url)
    url = "https://hqbuff.com/api/uk/" + url

    headers = {"user-agent": "questionScrape"}
    req = requests.get(url, headers)
    req.encoding = 'utf-8'

    data = json.loads(req.text)

    # loop through every game
    for game in data:
        # we only care about the question key
        for question in game['questions']:
            if not is_valid_question(question):
                continue

            category = question['category_slug']
            if category == '':
                category = 'general-knowledge'
            if category not in categorised_qs:
                q_list = []
                categorised_qs[category] = q_list
            else:
                q_list = categorised_qs[category]

            answers = []
            correct = 0
            title = sanitise(question['text'])
            question_number = question['question_number']
            # loop through all answers, store the correct one
            for i, ans in enumerate(question['answers']):
                answers.append(sanitise(ans['text']))
                if ans['correct']:
                    correct = i

            # write the final output to the file
            q_list.append('"' + title + '",' + ','.join(map('"{0}"'.format, answers)) + ',' + str(correct) + ',' + str(question_number) + '\n')


def is_valid_question(question):
    return 'category_slug' in question and 'text' in question and 'answers' in question and 'question_number' in question


def sanitise(text):
    return text.replace('"', "'")

def write_data():
    for category in categorised_qs:
        f = codecs.open('questions/' + category + '.csv', 'w', 'utf-8')
        for question in categorised_qs[category]:
            f.write(question)
        f.close()


def main():
    # set url
    req = requests.get('http://hqbuff.com/uk')
    soup = BeautifulSoup(req.text, 'html5lib')
    # get all the games from hqbuff
    links = soup.find_all("ul", {"class": "list--archive"})[0]
    # slice the game urls to be in YYYY-MM-DD format
    all_games = [link.get('href')[9:19] for link in links.find_all('a')]

    # write the data for every question in the games to the file
    for link in all_games:
        write_one_game(link)  # we must prepend the url

    write_data()

main()