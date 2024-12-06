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

def get_rag_path():
    d = os.path.join(BASE_DIR, PATH_CONFIG['rag']['dir'])
    if not os.path.exists(d):
        os.makedirs(d)
    return d

def get_rag_raw_path():
    d = os.path.join(get_rag_path(), PATH_CONFIG['rag']['raw']['dir'])
    if not os.path.exists(d):
        os.makedirs(d)
    return d

def get_rag_processed_path():
    d = os.path.join(get_rag_path(), PATH_CONFIG['rag']['processed']['dir'])
    if not os.path.exists(d):
        os.makedirs(d)
    return d
