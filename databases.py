import sqlite3

db = sqlite3.connect('KyraDB.db')

def main():
    '''
        standard procedure:
    '''
    db.execute('DROP TABLE IF EXISTS Item')
    db.execute('''
    CREATE TABLE Item
    ( ItemID INTEGER PRIMARY KEY, Holding BOOLEAN, Room VARCHAR(20), X INT, Y INT, Inventory INT, Name TEXT);'''
    )    
    db.commit()
    
    db.execute('INSERT INTO Item ( Holding, Name ) VALUES ( ?, ? )', (True, 'Gem'))
    db.commit()
    
    
    x = db.execute('SELECT * FROM Item')
    for i in x:
        print i
    
def buildEventDivision():    
    '''
        build EventDivision table
    '''
    dList = []
    divs = db.execute('SELECT DivisionID FROM Event ORDER BY DivisionID')
    for d in divs:
        i = d[0].strip()
        if i not in dList:
            dList.append(i)
    
    for d in dList:
        db.execute('INSERT INTO EventDivision ( DivisionID, PrebracketID ) VALUES (?, ?)', (d, d))
    db.commit()
    
    x = db.execute('SELECT * FROM EventDivision')
    for i in x: print i

def joinDivision(a,b):
    '''
        join division a and b
    '''
    j = '{}/{}'.format(a,b)
    db.execute('UPDATE EventDivision SET PrebracketID = ? WHERE DivisionID = ? OR DivisionID = ?', (j,a,b))
    
    x = db.execute('SELECT * FROM EventDivision')
    for i in x: print i
    
def countPeopleInDivision():
    divs = db.execute('SELECT DivisionID FROM Event ORDER BY DivisionID')
    for d in divs:
        de = db.execute('SELECT FirstName,LastName,DivisionID FROM Event WHERE DivisionID = ?',(d[0],))
        count = db.execute('SELECT COUNT(DivisionID) FROM Event WHERE DivisionID = ?',(d[0],))
        for i in count: c = i[0]
        print "{}: {}".format(d[0], c)
        print ''
        for i in de: print "{} {}: {}".format(i[0],i[1],i[2])
    


     
def update():    
    Weight = 55
    db.execute("UPDATE {} SET LastName = ? WHERE FighterID = ?".format('Fighter'), ('frost',1 ))
    db.commit()
    
    cursor = db.execute('select * from Fighter')
    for row in cursor:
        print row
    
def read():
    cursor = db.execute('SELECT FirstName,LastName,Gym FROM Fighter WHERE FirstName = ?',('jack',))
    cursor = db.execute('SELECT FirstName,LastName,Gym FROM Fighter WHERE FirstName = ? AND LastName = ?',('jack','frost'))
    for row in cursor:
        print row
    
    cursor = db.execute('select * from Fighter')
    for row in cursor:
        print row
        
def populateEvent():
    entries = [
    dict(FirstName = 'Jack',LastName = 'Frost',Gym = 'Arctic',Preweight = 82,Age = 2009,Sex = 'Male',AgeClass = 'Masters',Rank = 'Frosty Wizard Guy'),
    dict(FirstName = 'Magilla',LastName = 'Gorilla',Gym = 'Zoo',Preweight = 1002,Age = 12,Sex = 'Male',AgeClass = 'Youth',Rank = 'Gorilla'),
    dict(FirstName = 'Fred',LastName = 'Astaire',Gym = 'Dance Studio',Preweight = 132,Age = 39,Sex = 'Male',AgeClass = 'Masters',Rank = 'Dance Wizard'),
    dict(FirstName = 'Audrey',LastName = 'Hepburn',Gym = 'Danish Resistance',Preweight = 112,Age = 19,Sex = 'Female',AgeClass = 'Womens',Rank = 'Ballerina'),
    dict(FirstName = 'Humpty',LastName = 'Dumpty',Gym = 'The Wall',Preweight = 162,Age = 26,Sex = 'Male',AgeClass = 'Mens',Rank = 'Egg Man')
    ]
    for entry in entries:
        insertEntry(entry)

def delete(table, value, condition):
    db = sqlite3.connect('FightPrototype.db')
    db.execute("DELETE FROM {} WHERE ? = ?".format(table), (value, condition))
    db.commit()
    
    cursor = db.execute('select * from {}'.format(table))
    for row in cursor:
        print row

def insertEntry(row):
    '''
        takes entry dictionary and inserts entry to Event table
    '''
    
    fn = row['FirstName']
    ln = row['LastName']
    g = row['Gym']
    w = row['Preweight']
    a = row['Age']
    ac = row['AgeClass']
    s = row['Sex']
    r = row['Rank'] 
    
    db = sqlite3.connect('FightPrototype.db')
    db.execute("INSERT INTO Event (FirstName, LastName, Gym, Age, AgeClass, Preweight, Sex, Rank, Added) VALUES (?, ?, ?, ?, ?, ?, ?, ?, DATETIME('now'))",(fn,ln,g,a,ac,w,s,r) )
    db.commit()
    
def insertFighter(row):
    '''
        takes entry dictionary and inserts entry to Fighter table
    '''
    
    fn = row['FirstName']
    ln = row['LastName']
    g = row['Gym']
    w = row['Weight']
    a = row['Age']
    s = row['Sex']
    r = row['Rank'] 
    
    db = sqlite3.connect('FightPrototype.db')
    db.execute("INSERT INTO Fighter (FirstName, LastName, Gym, Age, Weight, Sex, Rank, Added) VALUES (?, ?, ?, ?, ?, ?, ?, DATETIME('now'))",(fn,ln,g,a,w,s,r) )
    db.commit()
    
    cursor = db.execute('select * from Fighter WHERE LastName = ?',(ln,))
    for row in cursor:
        print row
    
def rebuildDB():
    '''
        drops all tables and rebuilds empty DB
        use with caution
    '''
    
    db = sqlite3.connect('FightPrototype.db')
    

    
    db.execute('''
    CREATE TABLE EventInfo 
    ( EventID INTEGER PRIMARY KEY, Date DATE, Location TEXT, Fee INT, Ruleset VARCHAR(20), EventName VARCHAR(30) UNIQUE);'''
    )
    db.execute('''
    CREATE TABLE EventDivision
    ( DivisionID VARCHAR(30), PrebracketID VARCHAR(30) );'''
    )
    db.execute('''
    CREATE TABLE Match
    ( MatchID INTEGER PRIMARY KEY, Won INTEGER, Lost INTEGER, VictoryType VARCHAR(15), Points INT, Duration INT, DivisionID VARCHAR(30), EventID INT, Date DATETIME );'''
    )
    db.execute('''
    CREATE TABLE Event
    ( EntryID INTEGER PRIMARY KEY, FirstName TEXT, LastName TEXT, Gym Text, Age INT, AgeClass TEXT, Preweight REAL, Postweight REAL, Sex TEXT, Rank TEXT, DOB DATE, FighterID INTEGER, EventID INTEGER, DivisionID VARCHAR(30), Waiver BOOLEAN, Trainer VARCHAR(30), Fee INT, Win INT, Lose INT, Added DATETIME );  '''
    )
    db.execute('''
    CREATE TABLE Fighter
    ( FighterID INTEGER PRIMARY KEY, FirstName TEXT, LastName TEXT, Gym Text, Age INT, Weight REAL, Sex TEXT, Rank TEXT, DOB DATE, Image BLOB, Added DATETIME);'''
    )
    
    db.commit()
    getMaster(db)
    
def getMaster(db):
    '''
        prints DB master
    '''
    
    cursor = db.execute('select * from sqlite_master')
    for row in cursor:
        if row[0] == 'table': print row[1], row[4]
    
if __name__ == '__main__':
    main()