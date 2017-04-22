#!/usr/bin/python

import recon
# from validate_email import validate_email
from database import database


def create_email(firstName, lastName, pattern):
    email = None
    dom = recon.domain
    if pattern == "fnamel@":
        email = firstName + "" + lastName[0] + "@" + dom
    elif pattern == "fnamelname@":
        email = firstName + "" + lastName + "@" + dom
    elif pattern == "fname.lname@":
        email = firstName + "." + lastName + "@" + dom
    elif pattern == "fname_lname@":
        email = firstName + "_" + lastName + "@" + dom
    elif pattern == "fname.l@":
        email = firstName + "." + lastName[0] + "@" + dom
    elif pattern == "f.lname@":
        email = firstName[0] + "." + lastName + "@" + dom
    elif pattern == "fname_l@":
        email = firstName + "_" + lastName[0] + "@" + dom
    elif pattern == "f_lname@":
        email = firstName[0] + "_" + lastName + "@" + dom
    elif pattern == "flname@":
        email = firstName[0] + "" + lastName + "@" + dom
    elif pattern == "fnameln@":
        email = firstName + "" + lastName[:2] + "@" + dom
    return email


def main():
    print "Creating emails"
    db = recon.comp + ".db"
    con = database.connect(db)
    names = open("profiles.txt", "r").read()
    patterns = open("patterns.txt", "r").read()
    for name in names:
        [fname, lname] = name.split(' ')
        for pattern in patterns:
            email = create_email(fname, lname, pattern)
            if validate_email(email):
                database.update_email(con, fname, lname, email)
                break
    print "Emails created"
