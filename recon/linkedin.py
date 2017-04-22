#!/usr/bin/python

import mechanize
from bs4 import BeautifulSoup

import recon
from database import database
from utils import logger, files

log = logger.getLogger()


class Profile():
    first_name = ""
    last_name = ""
    job = ""
    url = ""

    def __init__(self, firstName, lastName, job, url):
        self.first_name = firstName
        self.last_name = lastName
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
        return self.first_name + " " + self.last_name + ", " + self.job + " at " + recon.comp + " url profile " + self.url


# linkedin Login - with username and password
def login(br, username, password):
    log.info("Logging in to Linkedin...")
    br.form = list(br.forms())[0]
    br.form["session_key"] = username
    br.form["session_password"] = password
    response = br.submit()
    return response


# Search Company
def searchCompany(br, query):
    response = None;

    try:
        log.info("Searching for company {}".format(recon.comp))
        br.select_form(nr=0)
        br.form["keywords"] = "companies: " + recon.comp
        response = br.submit()

    except Exception, e:
        log.error("function {} caught exception: - Might be issue with your login. Exception: {}".format(
            searchCompany.__name__, str(e)))
        exit(2)

    finally:
        return response


# Extract the Company Linkedin Web Site
def extractCompany(response):
    soup = BeautifulSoup(response.read(), "html.parser")

    mainDiv = soup.find_all("div", {"id": "srp_main_"})
    mainDiv = mainDiv.__str__().split(":")

    companyList = list()

    # add all companies to list
    for item in mainDiv:
        if "vsrp_companies_res_name" in item:
            temp = item.split(",")
            temp = temp[0].split('"')
            companyList.append("https://www.linkedin.com" + temp[1])
            break

    # currenlty assuming that first company is the wanted one
    log.debug("company link is " + companyList[0])
    return companyList[0]


# Extract the "SEE ALL" Page in order crawl employees
def seeAllCompanyEmployees(br, company):
    soup = BeautifulSoup(br.open(company).read(), "html.parser")

    log.debug("Getting See All Page of company " + company)

    # find deepest relevant div
    mainDiv = soup.find_all("div", {"id": "extra"})

    # soup the specific div
    soup = BeautifulSoup(mainDiv.__str__(), "html.parser")

    # find all divs
    mainDiv = soup.find_all("div")

    # extract all links from div
    all = mainDiv[0].__str__().split("href")

    # extract relevant link (contains the See all phrase)
    for item in all:
        if "See all" in item:
            each = item.split('"')
            break

    if each != None:
        seeAllPage = "https://www.linkedin.com" + each[1]
        return seeAllPage
    else:
        print "Error"
        return


# Extract Next Page
# return None in case of no "next page"
def extractNextPage(div):
    try:

        nextPage = div[0].__str__().split("nextPage")
        nextPage = nextPage[1].__str__().split(",")
        nextPage = nextPage[1].split(":")
        nextPage = nextPage[1].split('"')
        nextPage = "https://www.linkedin.com" + nextPage[1]

        log.debug("next page is " + nextPage)

        return nextPage

    except Exception, e:
        log.debug("could not get next page returning none")
        return None


# Extract Profiles from a given page
def extractProfiles(profilesDiv):
    con = database.connect(recon.comp + ".db")
    profiles = 0

    try:
        profilesDiv = profilesDiv[0].__str__().split(",")

        firstName = ""
        link = ""
        lastName = ""
        job = ""
        valid = False

        # loop to find all relevant people
        for item in profilesDiv:

            if "fNameP" in item:
                firstName = item.split(":")
                firstName = firstName[1]
                # TODO: Check for empty string
                if len(firstName) > 3:
                    valid = True

            if "lNameP" in item:
                lastName = item.split(":")
                lastName = lastName[1]

            if "fmt_industry" in item:
                job = item.split(":")
                job = job[1]

            if "actions" in item and "https" in item:
                link = item.split(":")
                link = link[2] + ":" + link[3]

                p = Profile(firstName, lastName, job, link)
                # Insert to DB or to File
                if valid is True:
                    files.write_to_file("profiles.txt", firstName + lastName)
                    database.insert_employees_data(con, p.get_first_name(), p.get_last_name(), p.get_job(), "")
                    profiles += 1
                    valid = False

    except Exception, e:
        log.error("Exception caught in function {} {0}".format(extractProfiles.__name__, str(e)))

    finally:
        return profiles


def main(comp):
    log.info("Linkedin Module Started")

    # Init Mechanize params
    br = mechanize.Browser()
    br.set_handle_robots(False)
    cookies = mechanize.CookieJar()
    br.set_cookiejar(cookies)
    br.set_handle_redirect(True)
    br.set_handle_refresh(False)
    br.addheaders = [('User-agent', 'Firefox')]

    # Linked in Params
    url = "https://www.linkedin.com/"
    br.open(url)
    user = "samm8500@walla.co.il"
    password = "road1953"

    # Login
    login(br, user, password)

    # Search for related company
    response = searchCompany(br, comp)

    # Get first company in search
    company = extractCompany(response)

    # Get first page of company employees - through the "See All" page
    seeAllPage = seeAllCompanyEmployees(br, company)

    # Extract profiles and the next page of profiles
    # first page for searching profiles is the "see all page"
    nextPage = seeAllPage

    loopCount = 1  # to count number of pages crawled
    profilesExtracted = 0  # to count number of profiles crawled

    # loop over pages and extract profiles
    while not nextPage is None:
        try:
            soup = BeautifulSoup(br.open(nextPage).read(), "html.parser")
            mainDiv = soup.find_all('div', {'id': 'srp_main_'})

            # get next page of next loop
            nextPage = extractNextPage(mainDiv)

            # Extract employees from page
            profilesExtracted += extractProfiles(mainDiv)
            loopCount += 1

        except Exception, e:
            log.error("caught exception " + str(e) + " " + nextPage)
            break

    # Summary
    log.info("Went through {} pages, and extracted {} people".format(loopCount, profilesExtracted))

    log.info("Linkedin Module Ended")
