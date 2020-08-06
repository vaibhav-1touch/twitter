import os
import random
import time
import pickle
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains

search_keyword = ""

# Functions in order ->
# get_cookies()             Load cookies from previous session with cookies.pkl file
# save_cookies()            Save cookies for current session to cookies.pkl
# get_account()             Get a single user handle from account.txt
# login()                   Enter user credentials on login page
# search_bar()              Searches the user handle and open main page
# open_followers()          Click on followers button to open the followers scroll menu
# random_follow()           Follow random ids and get names from followers button and save it to account.txt


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
    global search_keyword

    if search_keyword == "":
        name = []
        with open('accounts.txt','r') as f:
            name = f.read().split('\n')
            search_keyword = name[0]
            user_handle = name[0]

        name.remove(name[0])
        name = [x for x in name if x]
        with open('accounts.txt','w') as f:
            for i in name:
                f.write(i)
                f.write('\n')


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

    list_child_class = ".css-4rbku5.css-1dbjc4n.r-1ny4l3l.r-1j3t67a.r-1w50u8q"
    list_class = driver.find_elements_by_css_selector(list_child_class)
    for i in list_class:
        if i.get_attribute('data-testid') == "TypeaheadUser":
            parent = i.find_element_by_xpath('..')
            i.click()
            break

    time.sleep(random.randint(4, 5) + random.random())
    

def open_followers():
    follow_button_child_div_class = ".css-901oao.css-16my406.r-1qd0xha.r-vw2c0b.r-ad9z0x.r-bcqeeo.r-qvutc0"
    name = 'https://twitter.com/' + search_keyword + '/followers'
    for i in driver.find_elements_by_css_selector(follow_button_child_div_class):
        elem = i.find_element_by_xpath('..')
        print(elem.get_attribute('href'))
        if elem.get_attribute('href') == name:
            ActionChains(driver).move_to_element(i).click().perform()
            break

    time.sleep(random.randint(4, 5) + random.random())
    

def random_follow():
    div_class_followers_list = ".css-1dbjc4n.r-1awozwy.r-18u37iz.r-1wtj0ep"

    div_name_class = driver.find_elements_by_css_selector(".css-1dbjc4n.r-1wbh5a2.r-dnmrzs")
    div_followers_class = driver.find_elements_by_css_selector(".css-1dbjc4n.r-1n0xq6e.r-bcqeeo")
    count = 0
    accounts =  []
    for i in driver.find_elements_by_css_selector(div_class_followers_list):
        for j, k in zip(div_name_class, div_followers_class):

            for names in j.find_elements_by_tag_name('a'):
                accounts.append(names.get_attribute("href").strip("https://twitter.com/"))
                print(f'Following {names.get_attribute("href").strip("/")}')

            for button in k.find_elements_by_xpath('//div'):
                if button.get_attribute('role') == "button":
                    for m in button.find_elements_by_tag_name('span'):
                        print(m.text)
                        if m.text == "Follow" and count < 5 and random.random() > 0.7:
                            ActionChains(driver).move_to_element(m).click().perform()
                            time.sleep(random.randint(2,4) + random.random())
                            count += 1
                            break
    
    with open('accounts.txt', 'a') as f:
        for i in accounts:
            f.write(i)
            f.write('\n')
        


if __name__ == "__main__":
    get_account()
    print(search_keyword)
    get_cookies()
    login()
    save_cookies()
    search_bar(search_keyword)
    open_followers()
    random_follow()