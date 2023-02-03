import sqlite3

def dbcon():
    return sqlite3.connect("notary.db", check_same_thread=False)

