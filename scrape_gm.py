#!/usr/bin/env python

'''
Run the google maps popularity scraper
'''

from email import header
import os
import sys
import re
import time
import json
import urllib.parse
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup
from datetime import datetime
import pandas as pd

# load local params from config.py
import config

# gmaps starts their weeks on sunday
days = ['Sunday', 'Monday', 'Tuesday',
        'Wednesday', 'Thursday', 'Friday', 'Saturday']

# generate unique runtime for this job
run_time = datetime.now().strftime('%Y%m%d_%H%M%S')


def main():
    print('run_time:', run_time)
    # # read the list of URLs from a URL, or path to a local csv
    # if not config.DEBUG:
    # 	if len(sys.argv) > 1:
    # 		# read path to file from system arguments
    # 		urls = pd.read_csv(sys.argv[1])
    # 	else:
    # 		# get path to file from config.py
    # 		urls = pd.read_csv(config.URL_PATH_INPUT)
    # else:
    # 	# debugging case
    # 	print('RUNNING TEST URLS...')
    # 	urls = pd.read_csv(config.URL_PATH_INPUT_TEST)

    # # write to folder logs to remember the state of the config file
    # urls.to_csv('logs' + os.sep + run_time + '.log', index = False)

    # print(urls)

    # url_list = urls.iloc[:, 0].tolist()

    ###
    # document.querySelectorAll('div[aria-label*="Results"] a')
    # Array.from(document.querySelectorAll('div[aria-label*="Results"] a')).map(a => a.href)

    with open('google_urls/supermarket_nearby_stuttgart.json', 'r') as f:
        urls = json.load(f)
    url_list = [item for sublist in urls for item in sublist]

    # url_list = [
    #     "https://www.google.com/maps/place/BLOCK+HOUSE+Eberhardstra%C3%9Fe/data=!4m5!3m4!1s0x4799db4ba38c358d:0xa76428dedf249d6f!8m2!3d48.773482!4d9.177899?authuser=0&hl=en&rclk=1", "https://www.google.com/maps/place/Platzhirsch/data=!4m5!3m4!1s0x4799db4bb9f7dc07:0xaba291b8793796b6!8m2!3d48.7736236!4d9.1770435?authuser=0&hl=en&rclk=1", "https://www.google.com/maps/place/Thios+Inn/data=!4m5!3m4!1s0x4799db4b75470f73:0x77b941d2f0d37445!8m2!3d48.7729582!4d9.1777421?authuser=0&hl=en&rclk=1", "https://www.google.com/maps/place/Wilma+Wunder+Stuttgart/data=!4m5!3m4!1s0x4799dbaa7bae7f3b:0xd290613f570c4291!8m2!3d48.77445!4d9.1722868?authuser=0&hl=en&rclk=1", "https://www.google.com/maps/place/Restaurant+R%C3%B6sch/data=!4m5!3m4!1s0x4799db6c3bdcec27:0x777ac3ec284cd594!8m2!3d48.774931!4d9.1476508?authuser=0&hl=en&rclk=1", "https://www.google.com/maps/place/Alte+Kanzlei/data=!4m5!3m4!1s0x4799db3590f66031:0x9cd8cf5a853d3137!8m2!3d48.7774891!4d9.1786788?authuser=0&hl=en&rclk=1", "https://www.google.com/maps/place/Wirtshaus+Lautenschlager/data=!4m5!3m4!1s0x4799db2aaa591b23:0x373fe3bc31504fef!8m2!3d48.7808151!4d9.1775009?authuser=0&hl=en&rclk=1", "https://www.google.com/maps/place/BLOCK+HOUSE+Arnulf-Klett-Platz/data=!4m5!3m4!1s0x4799db3376a9e25b:0x3342fbfc76b5c99a!8m2!3d48.7830435!4d9.1802602?authuser=0&hl=en&rclk=1", "https://www.google.com/maps/place/Speisekammer+West/data=!4m5!3m4!1s0x4799db6adf452327:0x1ff5d557c92b5cca!8m2!3d48.7777774!4d9.1540726?authuser=0&hl=en&rclk=1", "https://www.google.com/maps/place/BLOCK+HOUSE+Eberhardstra%C3%9Fe/data=!4m5!3m4!1s0x4799db4ba38c358d:0xa76428dedf249d6f!8m2!3d48.773482!4d9.177899?authuser=0&hl=en&rclk=1", "https://www.google.com/maps/place/Triple+B+-+Beef+Burger+Brothers/data=!4m5!3m4!1s0x4799db4923883d17:0xcb286de02d57b417!8m2!3d48.7729712!4d9.1722876?authuser=0&hl=en&rclk=1", "https://www.google.com/maps/place/DO's+Vietnam+Street+Food/data=!4m5!3m4!1s0x4799db4bfe2a3cc3:0x890f73257ea42329!8m2!3d48.7721876!4d9.1745607?authuser=0&hl=en&rclk=1", "https://www.google.com/maps/place/tobi%E2%80%99s+Restaurant/data=!4m5!3m4!1s0x4799db34262e96d7:0xe3972e58d9fd7e53!8m2!3d48.7799138!4d9.1771251?authuser=0&hl=en&rclk=1", "https://www.google.com/maps/place/Augustenst%C3%BCble/data=!4m5!3m4!1s0x4799db4327eeb2e7:0x8d2dc8003e83b5a3!8m2!3d48.7688889!4d9.1575?authuser=0&hl=en&rclk=1", "https://www.google.com/maps/place/AMADEUS+Restaurant+%26+Bar/data=!4m5!3m4!1s0x4799db4ab2ed0705:0x792fa87131d4292a!8m2!3d48.77576!4d9.182181?authuser=0&hl=en&rclk=1", "https://www.google.com/maps/place/Restaurant+Zeppelino%E2%80%99S/data=!4m5!3m4!1s0x4799db33b8cf3491:0x887ce62e1d55160f!8m2!3d48.783293!4d9.179945?authuser=0&hl=en&rclk=1", "https://www.google.com/maps/place/Enchilada+Stuttgart/data=!4m5!3m4!1s0x4799db4be7455d6f:0xb6f40bd6645a7851!8m2!3d48.7730659!4d9.1753052?authuser=0&hl=en&rclk=1", "https://www.google.com/maps/place/Ochs'n+Willi/data=!4m5!3m4!1s0x4799db35e7ef0543:0xa9cbb2774e279e7a!8m2!3d48.7780805!4d9.1769307?authuser=0&hl=en&rclk=1", "https://www.google.com/maps/place/Carls+Brauhaus/data=!4m5!3m4!1s0x4799db34ff6c6b77:0x90c6c1bff759b0aa!8m2!3d48.7794633!4d9.1799805?authuser=0&hl=en&rclk=1", "https://www.google.com/maps/place/Sen+Viet+Restaurant/data=!4m5!3m4!1s0x4799c4d9b2df22af:0xb3a28c7978dcd995!8m2!3d48.7925!4d9.2027778?authuser=0&hl=en&rclk=1", "https://www.google.com/maps/place/Burger+House/data=!4m5!3m4!1s0x4799db36326e55eb:0x780896b065625245!8m2!3d48.7777239!4d9.1733751?authuser=0&hl=en&rclk=1"
    #     # "https://www.google.de/maps/place/Der+Grüne+Libanon/@47.3809037,8.5325491,17z/data=!3m1!4b1!4m5!3m4!1s0x47900a0e662015b7:0x54fec14b60b7f528!8m2!3d47.3808658!4d8.5347991",
    #     # "https://www.google.com/maps/place/Amboss+Rampe/@47.3809073,8.5325491,17z/data=!4m12!1m6!3m5!1s0x47900a0e662015b7:0x54fec14b60b7f528!2sAl-Mouchtar!8m2!3d47.3808658!4d8.5347991!3m4!1s0x47900a11e6035143:0x590c48610ac79170!8m2!3d47.3811339!4d8.5318852"
    # ]
    for url in url_list:
        print(urllib.parse.urlparse(url))
        print(url)

        try:
            title, data = run_scraper(url)
        except:
            print('ERROR:', url, run_time)
            # go to next url
            continue

        if len(data) > 0:
            # valid data to be written
            file_name = sanitize_filename(title)

            with open('data' + os.sep + file_name + '.json', 'w') as f:
                json.dump(data, f)

            print('DONE:', url, run_time)

        else:
            print('WARNING: no data', url, run_time)


def sanitize_filename(s):
	return urllib.parse.unquote(s).replace('+', '_').replace('?', '_')


def run_scraper(u):

    # because scraping takes some time, write the actual timestamp instead of the runtime
    scrape_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print('scrape_time:', scrape_time)

    # get html source (note this uses headless Chrome via Selenium)
    html = get_html(u, 'html' + os.sep + make_file_name(u) + '.' + '.html')

    # parse html (uses beautifulsoup4)
    title, data = parse_html(html)

    return title, data


def make_file_name(u):
    # generate filename from gmaps url
    # TODO - maybe clean this up

    try:
        file_name = u.split('/')[5].split(',')[0]
        file_name = urllib.parse.unquote(
            file_name).replace('+', '_').replace('?', '_')
    except:
        # maybe the URL is a short one, or whatever
        file_name = u.split('/')[-1]
        file_name = urllib.parse.unquote(
            file_name).replace('+', '_').replace('?', '_')
    # print(file_name)

    #file_name = file_name + '.' + run_time

    return file_name


def get_html(u, file_name):

    # if the html source exists as a local file, don't bother to scrape it
    # this shouldn't run
    if os.path.isfile(file_name):
        with open(file_name, 'r') as f:
            html = f.read()
        return html

    else:
        # requires chromedriver
        options = webdriver.ChromeOptions()
        # options.add_argument('--start-maximized')
        # options.add_argument('--headless')
        # https://stackoverflow.com/a/55152213/2327328
        # I choose German because the time is 24h, less to parse
        options.add_argument('--lang=de-DE')
        d = webdriver.Chrome()

        # get page
        d.get(u)

        d.find_element_by_xpath('//form //button').click()

        # sleep to let the page render, it can take some time
        # timeout after max N seconds (config.py)
        # based on https://stackoverflow.com/questions/26566799/wait-until-page-is-loaded-with-selenium-webdriver-for-python
        # try:
        # 	WebDriverWait(d, config.SLEEP_SEC).until(EC.text_to_be_present_in_element((By.TAG_NAME, 'h2'), 'Popular'))
        # except TimeoutException:
        # 	print('ERROR: Timeout! (This could be due to missing "popular times" data, or not enough waiting.)',u)
        time.sleep(5)

        # save html local file
        if config.SAVE_HTML:
            with open(file_name, 'w') as f:
                f.write(d.page_source)

        # save html as variable
        html = d.page_source

        d.quit()
        return html


def convert_12hour_to_24hour(hour, period):
    # convert 12 hour time to 24 hour time
    # based on https://stackoverflow.com/a/15470128/2327328
    if period == 'am':
        if hour == 12:
            hour = 0
    else:
        if hour != 12:
            hour = hour + 12

    return hour


def parse_html(html):
    soup = BeautifulSoup(html, features='html.parser')

    title = soup.find('h1', {'class': 'gm2-headline-5'})
    title = title.parent.parent
    title_h1 = title.find('h1')
    title_h2 = title.find('h2')

    title = title_h1.text.strip() + ' - ' + (title_h2.text.strip() if title_h2 else '')
    print(title)

    header_pop = soup.find(lambda tag: tag.name ==
                           "h2" and "Popular times" in tag.text)
    print('header_pop:', header_pop)
    div_pop = header_pop.parent.parent
    print(div_pop['aria-label'])

    pops = div_pop.find_all(lambda tag: tag.name == "div" and tag.has_attr(
        'aria-label') and "busy" in tag['aria-label'])
    data = [[0 for i in range(24)] for j in range(7)]

    for pop in pops:
        # note that data is stored sunday first, regardless of the local
        t = pop['aria-label']
        p = pop.parent.parent

        day = re.findall(r'\d+', p['jsinstance'])[0]

        busy_pattern = re.findall(r'(\d+)%.*?(\d+).(\w+)', t)
        if not busy_pattern:
            continue
        busy, hour, period = busy_pattern[0]

        day = int(day)
        busy = float(busy) / 100
        hour = convert_12hour_to_24hour(int(hour), period)

        print(int(day), hour, busy)

        data[day][hour] = busy

    return title, data


if __name__ == '__main__':
    main()
