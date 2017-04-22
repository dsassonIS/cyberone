#!/usr/bin/python

from validate_email import validate_email

import recon
from database import database
from utils import files


def analyze(results):
    pattern = ""
    for result in results:
        if '.' in result:
            [a, b] = result.split('.')
            if a > 1:
                a = "fname"
            else:
                f = "a"
            if b > 1:
                b = "lname"
            else:
                b = "l"
            pattern = a + "." + b + "@"
        elif '_' in result:
            [a, b] = result.split('_')
            if a > 1:
                a = "fname"
            else:
                f = "a"
            if b > 1:
                b = "lname"
            else:
                b = "l"
            pattern = a + "_" + b + "@"
        else:
            pass
    return pattern


def generate_emails(pattern):
    print "Creating emails"
    db = recon.comp + ".db"
    con = database.connect(db)
    names = files.read_file("profiles.txt")
    for name in names:
        [fname, lname] = name.split(' ')
        email = create_email(fname, lname, pattern)
        if validate_email(email):
            database.insert_employees_data(con, fname, lname, "", email)
    print "Emails created"


def create_email(firstName, lastName, pattern):
    email = None
    site = recon.domain
    if pattern == "fnamel@":
        email = firstName + "" + lastName[0] + "@" + site
    elif pattern == "fnamelname@":
        email = firstName + "" + lastName + "@" + site
    elif pattern == "fname.lname@":
        email = firstName + "." + lastName + "@" + site
    elif pattern == "fname_lname@":
        email = firstName + "_" + lastName + "@" + site
    elif pattern == "fname.l@":
        email = firstName + "." + lastName[0] + "@" + site
    elif pattern == "f.lname@":
        email = firstName[0] + "." + lastName + "@" + site
    elif pattern == "fname_l@":
        email = firstName + "_" + lastName[0] + "@" + site
    elif pattern == "f_lname@":
        email = firstName[0] + "_" + lastName + "@" + site
    elif pattern == "flname@":
        email = firstName[0] + "" + lastName + "@" + site
    return email


def main():
    results = files.read_file("emails.txt")
    pattern = analyze(results)
    generate_emails(pattern)
