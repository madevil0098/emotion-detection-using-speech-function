from code.db.dbConn import getConnection
import uuid
from datetime import datetime

# Get Single Sessions
def getSession(id):
    try:
        cnn = getConnection()
        query = "select * from session where session_id='{}'".format(id)
        cr = cnn.cursor()
        cr.execute(query)
        record = cr.fetchone()
        cnn.close()
        return record
    except Exception as ex:
        print(ex)    
        return False

# Get all Sessions
def getAllSessions(startposition):
    try:
        cnn = getConnection()
        query = "select * from session LIMIT 10 OFFSET {}".format(startposition)
        cr = cnn.cursor()
        cr.execute(query)
        records = cr.fetchall()
        cnn.close()
        return records
    except Exception as ex:
        print(ex)    
        return False
#Create New Session
def createSession(title):
    try:
        cnn = getConnection()
        session_uuid = uuid.uuid1()    
        date = datetime.now().strftime("%Y-%m-%d")    
        time = datetime.now().strftime("%H:%M:%S")    
        query = "insert into session(session_id,session_title,session_date,session_start_time) values('{}','{}','{}','{}')".format(session_uuid,title,date,time)
        cr = cnn.cursor()
        cr.execute(query)
        cnn.commit()
        cnn.close()
        return session_uuid
    except Exception as ex:
        print("Create Session Error : ",ex)    
        return None

def endSession(session_uuid):
    try:
        cnn = getConnection()     
        time = datetime.now().strftime("%H:%M:%S")    
        query = "update session set session_end_time='{}' where session_id='{}'".format(time,session_uuid)
        cr = cnn.cursor()
        cr.execute(query)
        cnn.commit()
        cnn.close()
        return True
    except Exception as ex:
        print("End Session Error : ",ex)    
        return False

def analysisDoneSession(session_uuid,faces):
    try:
        cnn = getConnection()     
        time = datetime.now().strftime("%H:%M:%S")    
        query = "update session set clusteringDone=true,noOfCluster={} where session_id='{}'".format(faces,session_uuid)
        
        cr = cnn.cursor()
        cr.execute(query)
        cnn.commit()
        cnn.close()
        return True
    except Exception as ex:
        print("End Session Error : ",ex)    
        return False

def recognitionDoneSession(session_uuid):
    try:
        cnn = getConnection()     
        time = datetime.now().strftime("%H:%M:%S")    
        query = "update session set analysisDone=true where session_id='{}'".format(session_uuid)
        cr = cnn.cursor()
        cr.execute(query)
        cnn.commit()
        cnn.close()
        return True
    except Exception as ex:
        print("Update Session Error : ",ex)    
        return False        