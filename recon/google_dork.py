#!/usr/bin/python
# !/usr/bin/python

import re
import time
import urlparse
from urllib2 import HTTPError

import mechanize
from bs4 import BeautifulSoup


def get_links(br):
    html = br.response().read()
    soup = BeautifulSoup(html, "lxml")
    links = []
    for a in soup.select('.r a'):
        href = urlparse.parse_qs(urlparse.urlparse(a['href']).query)['q'][0]
        links.append(href)
        print href
    return links


def search_emails(br, links):
    global email
    print links
    emails = []
    for link in links:
        br.open(link)
        html = br.response().read()
        # regex = re.compile(("([a-z0-9!#$%&'*+\/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+\/=?^_`"
        #					"{|}~-]+)*(@|\sat\s)(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?(\.|"
        #					"\sdot\s))+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?)"))
        p = re.compile(r'[\w\-][\w\-\.]+@[\w\-][\w\-\.]+[a-zA-Z]{1,4}')
        emails.append(re.findall(p, html))
        print emails
        res = []
        # for each in emails:
        #	res.append(each[0])
        time.sleep(5)
    emails = sorted(set(emails))
    return emails


def main(domain):
    print "Start dorking..."
    email = "@" + domain
    br = mechanize.Browser()
    cookies = mechanize.CookieJar()
    br.set_handle_robots(False)
    br.set_cookiejar(cookies)
    br.addheaders = [('User-agent', 'Mozilla/5.0')]
    search = "site:" + domain + "+intext:'" + email + "'"
    url = "http://www.google.com/search?q=" + search
    try:
        br.open(url)
    except HTTPError, e:
        print "Got error code", e.code
    links = get_links(br)
    time.sleep(5)
    print search_emails(br, links)
