"""
UTILITY CLASS TO READ THE LOCAL CONFIG.INI FILE AND PUT HOISTS
THEM GLOBALLY   
"""

import configparser

def read_config(config_file):
    """config reader method, pass the path to a .ini conventional
    config file."""
    global siis_backup, siis_path, db_host, db_port, db_username, db_password, show_warnings
    config = configparser.ConfigParser()
    config.read(config_file)
   
    # Reading values from the POSTGRESQL section
    db_host = config['POSTGRESQL']['host']
    db_port = config['POSTGRESQL']['port']
    db_username = config['POSTGRESQL']['username']
    db_password = config['POSTGRESQL']['password']
    db_name = config['POSTGRESQL']['database']

    # Reading values from the SIIS section
    siis_path = config['SIIS']['path']
    siis_backup = config['SIIS']['make_backup']

    # Reading values from the APPLICATION section
    show_warnings = config['APPLICATION']['verbose_warnings']
    return [siis_backup, siis_path, db_host, db_port, db_username, db_password, db_name, show_warnings]
