#!/usr/bin/python

import mechanize
from bs4 import BeautifulSoup

import recon
from database import database
from utils import files


class Profile():
    first_name = ""
    last_name = ""
    job = ""
    url = ""

    def __init__(self, name, job, url):
        self.first_name = name.split(' ')[0]
        self.last_name = name.split(' ')[1]
        self.job = job
        self.url = url

    # FIRST NAME
    def get_first_name(self):
        return self.first_name

    def set_first_name(self, first_name):
        self.first_name = first_name

    # LAST NAME
    def get_last_name(self):
        return self.last_name

    def set_last_name(self, last_name):
        self.last_name = last_name

    # JOB
    def get_job(self):
        return self.job

    def set_job(self, job):
        self.job = job

    # URL
    def get_url(self):
        return self.url

    def set_url(self, url):
        self.url = url

    # To String
    def __str__(self):
        return self.first_name + " " + self.last_name + ", " + self.job + " at " + recon.comp


def login(br, username, password):
    print "Logging in to Facebook..."
    br.select_form(nr=0)
    br.form['email'] = username
    br.form['pass'] = password
    br.submit()
    print "Logged in"


def search(br, query):
    res = br.open(query)
    soup = BeautifulSoup(res.read(), "lxml")
    soup.find_all('div', {'class': '_gll'})
    urls = []
    for profile in res:
        prof = profile.find('a')
        url = prof['href']
        url = url.replace('www', 'm')
        urls.append(url)
    return urls


def get_profiles(br, urls):
    con = database.connect(str(recon.comp + ".db"))
    for url in urls:
        res = br.open(url)
        soup = BeautifulSoup(res.read(), "lxml")
        name = soup.find_all('title')
        job = get_job(br, url)
        p = Profile(name, job, url)
        files.write_to_file("profiles.txt", name)
        database.insert_employees_data(con, p.get_first_name(), p.get_last_name(), p.get_job(), "")


def get_job(br, url):
    res = br.open(url)
    soup = BeautifulSoup(res.read(), "lxml")
    div = soup.find('span', {'class': 'dd de'})
    print div.text


def main(comp):
    br = mechanize.Browser()
    br.set_handle_robots(False)
    cookies = mechanize.CookieJar()
    br.set_cookiejar(cookies)
    br.set_handle_redirect(True)
    br.set_handle_refresh(False)
    br._factory.is_html = True
    hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64)', 'Connection': 'keep-alive'}
    br.addheaders = [hdr]
    url = "https://m.facebook.com/login.php"
    br.open(url)
    user = "fbuser7@walla.co.il"
    password = "passw0rdfb7"
    login(br, user, password)
    query = "https://www.facebook.com/search/str/People+who+work+at+" + comp + "/keywords_top"
    urls = search(br, query)
    get_profiles(br, urls)
