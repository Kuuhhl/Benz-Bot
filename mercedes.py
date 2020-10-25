import requests
import json
import time
from selenium import webdriver
baseurl = ('https://stagecast.se/api/quizzes/cd3d74fd-7539-4951-a408-144ed38dc00e/moments/6E0D2855-5D71-410B-9DE4-A34AC074BC9D/questions/')
def get_questions():
    f = open('questions.txt', 'a')
    x = 0
    while True:
        x = x + 1
        url = baseurl + str(x)
        r = requests.get(url, headers={'X-Token': 'JDJhJDEyJExrOGlUYThKZnBka3gubFJZRWMxT2VWVGkuVnVJUlRzdlgzLmthZWVya2oyUXFDSEROUjE2'})
        if r.status_code != 200:
            f.close()
            print('Fetched ' + str(x - 1) + ' questions.')
            print('Error message: ' + r.text)
            print('Response Code: ' + str(r.status_code))
            print('Failed link: ' + url)
            break
        f.write(r.text + '\n')
        print('Question ' + str(x) + ': ' + json.loads(r.text)['question']['text'])
def do_quiz(driver, f):
    questionasked = driver.find_element_by_class_name("question-text").text
    print(questionasked)
    choices = driver.find_elements_by_class_name("choice")
    text = f.readlines()
    for choice in choices:
        for x in range(len(text)):
            question = json.loads(text[x])['question']
            answer = json.loads(text[x])['right']
            if choice.text == answer:
                choice.click()
                time.sleep(5)
                do_quiz(driver, f)
    print('Not found.')
    thisdict = {
      "question": questionasked,
      "right": input('Please input the right answer: ')
    }
    fp = open('database.txt', 'a')
    fp.write(json.dumps(thisdict) + '\n')
    fp.close()
    do_quiz(driver, f)
def launch_quiz():
    f = open('database.txt', 'r')
    driver = webdriver.Chrome()
    driver.get("https://join.stagecast.se/api/web/code/3563/MTUsWCR4Mcu0ZaYwaL7qrHpTni9gK71yxZlq")
    time.sleep(2)
    driver.switch_to.frame(driver.find_element_by_id("frame"))
    driver.find_element_by_class_name("mc-checkmark").click()
    driver.find_element_by_class_name("main-button").click()
    driver.find_element_by_class_name("custom-button").click()
    time.sleep(5)
    do_quiz(driver, f)

def already_answered(question):
    fp = open('database.txt', 'r')
    text = fp.readlines()
    for x in range(len(text)):
        if json.loads(text[x])['question'] == question:
            fp.close()
            return True
    fp.close()

def get_answers():
    f = open('questions.txt', 'r')
    text = f.readlines()
    driver = webdriver.Chrome()
    
    for x in range(len(text)):
        question = json.loads(text[x])['question']['text']
        choices = json.loads(text[x])['choices']
        try:
            if already_answered(question) == True:
                continue
        except:
            pass
        print('Question number ' + str(x + 1) + ': ' + question)
        driver.get("https://www.google.com/search?q=" + question.replace(' ', '+'))
        for x in range(len(choices)):
            choice = choices[x]['value']
            print('Choice ' + str(x + 1) + ': ' + choice)
        response = input('Correct answer: ')
        if response == '':
            print("Okay, I'll skip this question.")
            print()
            continue
        right = choices[int(response) - 1]['value']
        thisdict = {
          "question": question,
          "right": right
        }
        fp = open('database.txt', 'a')
        fp.write(json.dumps(thisdict) + '\n')
        fp.close()
        print()
    f.close()
                
get_questions()
