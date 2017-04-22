#!/usr/bin/python

import urllib2
from urllib2 import HTTPError

import mechanize
from pyPdf import PdfFileReader

from database import database
from recon.google_dork import get_links


def printMeta(fileName):
    pdfFile = PdfFileReader(open(fileName, 'rb'))
    docInfo = pdfFile.getDocumentInfo()
    string = ""
    print '[*] PDF MetaData For: ' + str(fileName)
    for metaItem in docInfo:
        string += metaItem + ':' + docInfo[metaItem]
    return string


def downloadPDF(url):
    response = urllib2.urlopen(url)
    pdffile = open("document.pdf", 'w')
    pdffile.write(response.read())
    pdffile.close()
    return pdffile.name


def main(domain, db):
    con = database.connect(db)
    br = mechanize.Browser()
    cookies = mechanize.CookieJar()
    br.set_handle_robots(False)
    br.set_cookiejar(cookies)
    br.addheaders = [('User-agent', 'Mozilla/5.0')]
    search = "site:" + domain + "+type:pdf"
    url = "http://www.google.com/search?q=" + search
    try:
        br.open(url)
    except HTTPError, e:
        print "Got error code", e.code
    links = get_links(br)
    string = ""
    for link in links:
        if link.endswith(".pdf"):
            pdf_file = downloadPDF(link)
            string = printMeta(pdf_file)
            database.insert_metadata_data(con, pdf_file, string)
