import sqlite3
import os
from utilities import filehandles
from utilities import config


#handling config settings: 
cur_dir = os.getcwd()
config_file = os.path.join(cur_dir, 'config.ini')
siis_backup, siis_path, db_host, db_port, db_username, db_password, db_name, show_warnings = config.read_config(config_file)
siis_db = os.path.join(siis_path, 'SIIS_data','SIIS_database')
#connect to the local sqlite database: 
lite_conn = sqlite3.connect(os.path.join(siis_db, 'siis.db'))
lite_cursor = lite_conn.cursor()

filehandles.triggers_toggle(True, lite_conn)
print('Triggers are re-enabled! SIIS is safe to use.')