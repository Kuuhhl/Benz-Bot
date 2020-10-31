import requests
import datetime
import json
import time
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
import sys

##CONFIG
rankurl = ''
xtoken = ''
startingpageurl = ''

def do_quiz(driver, questionasked):
    answerdelay = 0.02
    o = 0
    while True:
        try:
            if questionasked == driver.find_element_by_class_name("question-text").text:
                raise
        except:
            continue
        a = datetime.datetime.now()
        questionasked = driver.find_element_by_class_name("question-text").text
        if questionasked != '':
            print('Question number ' + str(o + 1) + ': ' + questionasked)
        f = open('database.txt', 'r')
        text = f.readlines()
        for x in range(len(text)):
            question = json.loads(text[x])['question']
            answer = json.loads(text[x])['right']
            if questionasked == question:
                print('Answer: ' + answer)
                choices = driver.find_elements_by_class_name("choice")
                for choice in choices:
                    if choice.text == answer:
                        time.sleep(answerdelay)
                        secs = ((datetime.datetime.now() - a).seconds)
                        delay = answerdelay-secs
                        if o == 0:
                            delay = delay + 0.1
                        print('Delay: ' + str(delay) + 's')
                        print()
                        time.sleep(delay)
                        choice.click()
                        o = o + 1
                        if o > 6:
                            time.sleep(3)
                            position = json.loads(requests.get(rankurl, headers={'X-Token': xtoken}).text)['position']
                            print('Current rank: ' + str(position))
                            if position > 450:
                                print('Retrying to get to minimum of rank 450...')
                                print()
                                driver.quit()
                                launch_quiz()
                            else:
                                driver.quit()
                                sys.exit()
                f.close()
                continue
def launch_quiz():
    options = Options()
    #options.add_argument('--headless') #uncomment to try headless mode. Not tested yet, might be slower?
    driver = webdriver.Chrome(options=options)
    driver.get(startingpageurl)
    time.sleep(5)
    driver.switch_to.frame(driver.find_element_by_id("frame"))
    driver.find_element_by_class_name("mc-checkmark").click()
    driver.find_element_by_class_name("main-button").click()
    driver.find_element_by_xpath('//button[text()="Play Again "]').click()
    while True:
        try:
            print('Starting...')
            do_quiz(driver, None)
        except NoSuchElementException:
            continue
        break
launch_quiz()
