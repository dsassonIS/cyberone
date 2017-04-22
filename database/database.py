#!/usr/bin/python

import os
import sqlite3


def reset(name):
    # type: (object) -> object
    try:
        if os.path.exists(name + ".db"):
            os.remove(name + ".db")
    except WindowsError:
        print "database file is being used"
        exit(1)


def connect(db):
    con = sqlite3.connect(db)
    return con


'''

    EMPLOYEES TABLE

'''


def create_employees_table(con):
    with con:
        cur = con.cursor()
        cur.execute('CREATE TABLE Employees(FirstName TEXT, LastName TEXT, Job TEXT, Email TEXT)')
        print "Created table Employees"


def insert_employees_data(con, firstName, lastName, job, email):
    with con:
        cur = con.cursor()
        cur.execute("INSERT INTO Employees VALUES (?, ?, ?, ?)", (firstName, lastName, job, email))


def print_employees(con):
    with con:
        cur = con.cursor()
        cur.execute("SELECT * FROM Employees")
        rows = cur.fetchall()
        for row in rows:
            print row


def update_job(con, firstName, lastName, job):
    with con:
        cur = con.cursor()
        cur.execute("UPDATE Employees SET Job=? WHERE FirstName=? and LastName=?", (job, firstName, lastName))


def update_email(con, firstName, lastName, email):
    with con:
        cur = con.cursor()
        cur.execute("UPDATE Employees SET Email=? WHERE FirstName=? and LastName=?", (email, firstName, lastName))


'''

    HOSTS TABLE

'''


def create_hosts_table(con):
    with con:
        cur = con.cursor()
        cur.execute('CREATE TABLE Hosts(Domain TEXT, IP TEXT, Ports TEXT)')
        print "Created table Hosts"


def insert_hosts_data(con, domain, ip, ports):
    with con:
        cur = con.cursor()
        cur.execute("INSERT INTO Hosts VALUES (?, ?, ?)", (domain, ip, ports))


def update_hosts_domain(con, domain, ip):
    with con:
        cur = con.cursor()
        cur.execute("UPDATE Hosts SET Domain=? WHERE IP=?", (domain, ip))


def update_hosts_ip(con, ip, domain):
    with con:
        cur = con.cursor()
        cur.execute("UPDATE Hosts SET IP=? WHERE Domain=?", (ip, domain))


def update_hosts_ports(con, ports, ip):
    with con:
        cur = con.cursor()
        cur.execute("UPDATE Hosts SET Ports=? WHERE IP=?", (ports, ip))


def print_hosts(con):
    with con:
        cur = con.cursor()
        cur.execute("SELECT * FROM Hosts")
        rows = cur.fetchall()
        for row in rows:
            print row


'''

    METADATA TABLE

'''


def create_metadata_table(con):
    with con:
        cur = con.cursor()
        cur.execute('CREATE TABLE Metadata(Name TEXT, Data TEXT)')
        print "Created table Metadata"


def insert_metadata_data(con, name, data):
    with con:
        cur = con.cursor()
        cur.execute("INSERT INTO Metadata VALUES (?, ?)", (name, data))


def update_metadata_data(con, name, data):
    with con:
        cur = con.cursor()
        cur.execute("UPDATE Metadata SET Data=? WHERE Name=?", (data, name))


def print_metadata(con):
    with con:
        cur = con.cursor()
        cur.execute("SELECT * FROM Metadata")
        rows = cur.fetchall()
        for row in rows:
            print row
