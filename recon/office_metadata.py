from urllib2 import HTTPError

import mechanize

import recon
from database import database
from google_dork import get_links


def printMeta(fileName):
    res = os.system("python ")


def downloadFILE(link):
    pass


def main(domain):
    db = recon.comp + ".db"
    con = database.connect(db)
    br = mechanize.Browser()
    cookies = mechanize.CookieJar()
    br.set_handle_robots(False)
    br.set_cookiejar(cookies)
    br.addheaders = [('User-agent', 'Mozilla/5.0')]
    search = "site:" + domain + "+type:doc, docx, xls, ppt, pptx, xlsx"
    url = "http://www.google.com/search?q=" + search
    try:
        br.open(url)
    except HTTPError, e:
        print "Got error code", e.code
    links = get_links(br)
    for link in links:
        if link.endswith(".*"):
            pdf = downloadFILE(link)
            string = printMeta(pdf)
            database.insert_metadata_data(con, pdf, string)
