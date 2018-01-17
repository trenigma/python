'''
This script imports the sqlite3 module and establishes a connection
to the local database file 'emailorgcount.sqlite'. It then executes
a 'DROP TABLE IF EXISTS' statement for table 'Counts' so we begin with
a clean slate. It then creates a new table called 'Counts' to replace
it. 

When prompted for file name, input the local filename "mbox-short.txt"
sans quotes. The script will read through the file gathering email domain
or 'org' data and then execute an 'INSERT' command to add the data to the 
local database file.

Finally, the script executes a "SELECT' statement to return the count
for each line containing 'From: ' and the number of times each email 
address appears. Once this is complete, the script closes the connection
to the local database.
'''

import sqlite3

conn = sqlite3.connect('emailorgcount.sqlite')
cur = conn.cursor()

cur.execute('''
DROP TABLE IF EXISTS Counts''')

cur.execute('''
CREATE TABLE Counts (org TEXT, count INTEGER)''')

fname = input('Enter file name: ')
if ( len(fname) < 1 ) : fname = 'mbox-short.txt'
fh = open(fname)
for line in fh:
    if not line.startswith('From: ') : continue
    pieces = line.split()
    email = pieces[1]
    parts = email.split('@')
    org = parts[-1]
    cur.execute('SELECT count FROM Counts WHERE org = ? ', (org, ))
    row = cur.fetchone()
    if row is None:
        cur.execute('''INSERT INTO Counts (org, count) 
                VALUES ( ?, 1 )''', ( org, ) )
    else : 
        cur.execute('UPDATE Counts SET count=count+1 WHERE org = ?', 
            (org, ))
    conn.commit()

sqlstr = 'SELECT org, count FROM Counts ORDER BY count DESC LIMIT 10'

for row in cur.execute(sqlstr) :
    print(str(row[0]), row[1])

cur.close()
