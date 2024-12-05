import os

from config import CONFIG


PATH_CONFIG = CONFIG['core']['paths']

BASE_DIR = os.path.join(os.path.expanduser('~'), PATH_CONFIG['base']['dir'])
if not os.path.exists(BASE_DIR):
    os.makedirs(BASE_DIR)


def get_log_file_path():
    log_dir = PATH_CONFIG['logs']['dir']
    log_dir = os.path.join(BASE_DIR, log_dir)
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    return log_dir

def get_db_path():
    db_dir = os.path.join(BASE_DIR, PATH_CONFIG['db']['dir'])
    if not os.path.exists(db_dir):
        os.makedirs(db_dir)
    return os.path.join(db_dir, PATH_CONFIG['db']['name'])

def get_temp_path():
    temp_dir = os.path.join(BASE_DIR, PATH_CONFIG['temp']['dir'])
    if not os.path.exists(temp_dir):
        os.makedirs(temp_dir)
    return temp_dir

def get_docs_path():
    docs_dir = os.path.join(BASE_DIR, PATH_CONFIG['docs']['dir'])
    if not os.path.exists(docs_dir):
        os.makedirs(docs_dir)
    return docs_dir
