from tqdm import tqdm
import os
import sys
sys.path.append('utilities')
from datetime import datetime
from utilities import filehandles
from utilities import config
from utilities import interact
from utilities.structure import extract_pk_column
import sqlite3
import socket
import psycopg2
import psycopg2.extras


#handling config settings: 
cur_dir = os.getcwd()
config_file = os.path.join(cur_dir, 'config.ini')
siis_backup, siis_path, db_host, db_port, db_username, db_password, db_name, show_warnings = config.read_config(config_file)

#show warnings just to make sure!
if show_warnings:
    print('Before you continue verify the following: ')
    print('\t 1) SIIS is fully upsynced to the central database.')
    print('\t 2) SIIS has been closed without errors.')
    print('\t 3) SIIS triggers will be disabled during this update, \n if the program does not shut down in a controlled fashion you need re-enable these manually!.')
    print('')
    interact.checkInput('Y', 'N')

#make a backup of the original SIIS database, timestamp and zip it. 
siis_db = os.path.join(siis_path, 'SIIS_data','SIIS_database')
hostname = socket.gethostname()
now = datetime.now()
datetime_string = now.strftime("%Y-%m-%d %H.%M.%S")
zipname = hostname+'_'+datetime_string+'.zip'
zippath = os.path.join(cur_dir, 'backup', hostname, zipname)
filehandles.backup_database(siis_db, zippath)

#connect to the local sqlite database: 
lite_conn = sqlite3.connect(os.path.join(siis_db, 'siis.db'))
lite_cursor = lite_conn.cursor()


#####           CONNECTING TO DATABASES: 
#connect to the remote Postgresql database: 
# Database connection parameters
user = 'your_username'
password = 'your_password'
host = 'your_host'
port = 'your_port'  # default is '5432'

# Connect to the PostgreSQL database
pg_conn = psycopg2.connect(
    dbname=db_name,
    user=db_username,
    password=db_password,
    host=db_host,
    port=db_port
)
# Create a cursor object to interact with the database
pg_cursor = pg_conn.cursor(cursor_factory=psycopg2.extras.DictCursor)


#####           reading sync status and fetching new records to sync.: 
# get the id of last succesfull downsync record:
lite_cursor.execute("SELECT the_value FROM metadata WHERE metadata.the_key = 'last_downsync_number'")
last_sync = lite_cursor.fetchall()
if len(last_sync) == 0:
    #####MEANS: This toughbook did not yet perform a downsync, add the entry to the metadata table and start from 0
    last_sync = 0
    comment = 'automatically updated value indicating the last synchronised (server to client) record from change_log'
    key = 'last_downsync_number'
    visible = 1
    query = "INSERT INTO metadata VALUES (?,?,?,?,?)"
    data = [key, last_sync, None, comment, visible]
    print('This toughbook did not yet perform a downsync. Database update is required; continue? (Y/N)')
    interact.checkInput('Y', 'N')
    #create the metadata entry required for downsyncing!
    lite_cursor.execute(query, data)
    lite_conn.commit()

else:
    last_sync = last_sync[0][0]

# get all registered sync events from the PG server that have an id which is higher than last_sync: 
#       WARNING: order matters!
pg_new_sync_events = "SELECT * FROM change_log WHERE change_log.id > %s ORDER BY id ASC"
pg_cursor.execute(pg_new_sync_events, [last_sync])
sync_events = pg_cursor.fetchall()
filehandles.triggers_toggle(False, lite_conn)
#possible events: UPDATE, INSERT, DELETE
for event in tqdm(sync_events): 
    event = dict(event)
    eventid = event['id']
    action = event['the_action']
    table = event['on_table']
    rowid1 = event['on_id1']
    rowid2 = event['on_id2']
    #fetch the row from table by rowid1. 
    pks = extract_pk_column(table)
    whereslice = []
    whererestrict = []
    if rowid1 is not None: 
        whereslice.append(table+'."'+pks[0]+'" = %s')
        whererestrict.append(rowid1)
    if rowid2 is not None: 
        whereslice.append(table+'."'+pks[1]+'" = %s')
        whererestrict.append(rowid2)

    if action in ['UPDATE', 'INSERT']: 
        #   WARNING: id is NOT the default name for the PK field in all tables, some have other names!
        # fetch pk col: 
        fetch_pg_row = "SELECT * FROM "+table+" WHERE "+ ' AND '.join(whereslice)
        pg_cursor.execute(fetch_pg_row, whererestrict)
        rowdata = pg_cursor.fetchall()
        #extra check: did we really manage to find exactly ONE row, if we don't STOP the sync immediately!
        if len(rowdata) != 1:
            print('BUG detected, program will terminate.')
            print(fetch_pg_row)
            exit('QUERY CONSTRAINT FAILED ON REMOTE DATABASE TO IDENTIFY A SINGLE ROW.')
        #insert on conflict is not the best idea to use. We manually have to check if the row exists in the SQLITE DB:  
        #   reuse fetch_pg_row: 

        fetch_lite_row = fetch_pg_row.replace('%s', '?')
        exists_locally = lite_cursor.execute(fetch_lite_row, whererestrict)
        local_rows = lite_cursor.fetchall()
        if len(local_rows) == 1:
            #requires UPDATE
            new_values = []
            data = []
            for k,v in dict(rowdata[0]).items():
                new_values.append(f" {k} = ? ")
                data.append(v)
            lite_where = ' AND '.join(whereslice)
            column_updates = ', '.join(new_values)
            query = f" UPDATE " +table+ f" \
            SET {column_updates} \
            WHERE \
                "+ lite_where.replace('%s', '?')
            data.extend(whererestrict)
        elif len(local_rows) == 0:
            #requires INSERT
            data = rowdata[0]
            num_question_marks = len(data)
            question_marks_string = ', '.join(['?'] * num_question_marks)
            placeholders = '?'
            query = 'INSERT INTO '+table+ ' VALUES ('+question_marks_string+') '
        else:
            #requires exorcism.
            print('BUG detected, program will terminate.')
            print(fetch_lite_row)
            exit('QUERY CONSTRAINT FAILED ON LOCAL DATABASE TO IDENTIFY A SINGLE ROW.')
        lite_cursor.execute(query, data)
        lite_conn.commit()
    elif action == 'DELETE': 
        whereclause = ' AND '.join(whereslice)
        whereclause = whereclause.replace('%s', '?')
        lite_cursor.execute("DELETE FROM "+table+" WHERE "+whereclause, whererestrict)
        lite_conn.commit()
    else:
        print('Unsupported operation encountered', action)
        exit()
    #commit the action to the metadata table: 
    filehandles.update_last_downsync(eventid, lite_conn)



# Example query to verify connection (e.g., get the list of tables)
pg_cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public';")
tables = pg_cursor.fetchall()

filehandles.triggers_toggle(True, lite_conn)
print('SIIS database was closed succesfully and triggers are re-instated.')
print('You can now use SIIS again.')
# Close the cursor and connection
lite_cursor.close()
lite_conn.commit()
lite_conn.close()
pg_conn.close()