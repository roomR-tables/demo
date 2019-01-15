import os
import sqlite3
import app


if os.path.isfile('cc.db') is False:
    here = os.path.dirname(__file__)
    sqlinit = open(os.path.join(here, 'sql/schema.sql')).read()

    conn = sqlite3.connect('cc.db')
    conn.executescript(sqlinit)
    conn.close()

app.runApp()
