import os
import zipfile

def backup_database(source_dir, zip_file_path):
    # Ensure the destination directory exists
    os.makedirs(os.path.dirname(zip_file_path), exist_ok=True)
    
    # Open the zip file in append mode, create if it doesn't exist
    with zipfile.ZipFile(zip_file_path, 'a') as zipf:
        # Add each file in the source directory to the zip file
        for filename in os.listdir(source_dir):
            file_path = os.path.join(source_dir, filename)
            zipf.write(file_path, os.path.relpath(file_path, source_dir))


def update_last_downsync(id, conn):
    query = 'UPDATE metadata SET "the_value" = ? WHERE the_key = "last_downsync_number" '
    conn.execute(query, [id])
    conn.commit()

def triggers_toggle(use_triggers, conn):
    """
    True will enable the triggers on the database
    False will disable the triggers
    The metadata table of SIIS has a row with synclog, it accepts either active or disabled. 
    """
    if use_triggers == True: 
        query = 'UPDATE metadata SET "the_value" = "active" WHERE the_key = "synclog" '
    elif use_triggers == False: 
        query = 'UPDATE metadata SET "the_value" = "disabled" WHERE the_key = "synclog" '
    else:
        exit('Invalid command for triggers.')
    conn.execute(query)
    conn.commit()