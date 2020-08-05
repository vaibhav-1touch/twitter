import os
import random
import time
import pickle
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains

search_keyword = "TechnicalGuruji"


# Functions in order ->
# get_cookies()             Load cookies from previous session with cookies.pkl file
# save_cookies()            Save cookies for current session to cookies.pkl
# get_account()             Get a single user handle from account.txt
# login()                   Enter user credentials on login page
# search_bar()              Searches the user handle and open main page
# open_followers()          Click on followers button to open the followers scroll menu
# write_names()             Get names from followers button and save it to account.txt


load_dotenv()

option = Options()
# option.add_experimental_option("excludeSwitches", ["enable-automation"])
option.add_experimental_option("prefs", {"profile.default_content_setting_values.notifications": 1})
driver = webdriver.Chrome('chromedriver', options=option)
driver.get('https://twitter.com')
driver.maximize_window()


def get_cookies():
    if os.path.exists('cookies.pkl'):
        cookies = pickle.load(open('cookies.pkl', 'rb'))
        for cookie in cookies:
            driver.add_cookie(cookie)


def save_cookies():
    pickle.dump(driver.get_cookies(), open('cookies.pkl', 'wb'))


def get_account():
    name = []
    with open('accounts.txt','r') as f:
        name = f.read().split('\n')
        print(name[0])
        user_handle = name[0]

    print(name)
    # name.remove(name[0])
    name = [x for x in name if x]

    return name


def login():
    for i in driver.find_elements_by_tag_name('input'):
        if i.get_attribute('name') == "session[username_or_email]":
            for j in os.getenv('phone'):
                i.send_keys(j)
                time.sleep(0.5 * random.random())

        time.sleep(random.randint(1, 2) + random.random())

        if i.get_attribute('name') == "session[password]":
            for j in os.getenv('pass'):
                i.send_keys(j)
                time.sleep(0.5 * random.random())

            time.sleep(random.random())
            i.send_keys(Keys.ENTER)

    time.sleep(random.randint(3,5) + random.random())


def search_bar(search=search_keyword):
    for i in driver.find_elements_by_tag_name('input'):
        if i.get_attribute('placeholder') == "Search Twitter":
            ActionChains(driver).move_to_element(i).click().perform()
            time.sleep(random.randint(0, 2) + random.random())
            for j in search:
                i.send_keys(j)
                time.sleep(0.4 * random.random())
    
    time.sleep(random.randint(4, 6) + random.random())
    count = 0
    dropdown_accounts_div_class = ".css-1dbjc4n"
    for i in driver.find_elements_by_css_selector(dropdown_accounts_div_class):
        for j in i.find_elements_by_tag_name('div')[850:]:
            print(count)
            count += 1
            for k in j.find_elements_by_tag_name('span'):
                if j.get_attribute('role') == "button" and k.text.strip('@') == search_keyword:
                    ActionChains(driver).move_to_element(j).click().perform()
                    time.sleep(random.randint(4, 6) + random.random())
                    return


def open_followers():
    follow_button_parent_div_class = ".css-1dbjc4n.r-18u37iz.r-1w6e6rj"
    count = 0
    name = '/' + search_keyword + '/followers'
    print(name)
    for i in driver.find_elements_by_css_selector(follow_button_parent_div_class):
        for j in i.find_elements_by_tag_name('a'):
            print(count)
            count = count + 1
            print(j.get_attribute('href'))
            if j.get_attribute('href') == name:
                print('if loop worked')
                i.click()
                time.sleep(random.randint(1, 2) + random.random())
                return


def write_names():
    name_div_class = ".css-1dbjc4n.r-1wbh5a2.r-dnmrzs"

    names = driver.find_elements_by_css_selector(name_div_class)
    for i in names:
        for j in i.find_elements_by_tag_name('a'):
            print(j.get_attribute('href').strip('/'))


if __name__ == "__main__":
    # get_cookies()
    login()
    # save_cookies()
    search_bar()
    open_followers()
    write_names()
