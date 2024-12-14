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

def get_rag_metadata_json_path():
    return os.path.join(get_rag_path(), PATH_CONFIG['rag']['metadata']['name'])

def _get_rag_child_path(child):
    d = os.path.join(get_rag_path(), PATH_CONFIG['rag'][child]['dir'])
    if not os.path.exists(d):
        os.makedirs(d)
    return d

def get_rag_raw_path():
    return _get_rag_child_path('raw')

def get_rag_processed_path():
    return _get_rag_child_path('processed')

def get_rag_inverted_index_path():
    return _get_rag_child_path('inverted_index')

def get_rag_inverted_index_json_path():
    return os.path.join(get_rag_path(), PATH_CONFIG['rag']['inverted_index']['name'])

def get_rag_vector_db_path():
    return _get_rag_child_path('vector_db')

def get_rag_vector_db_json_path():
    return os.path.join(get_rag_path(), PATH_CONFIG['rag']['vector_db']['name'])

def get_rag_retiever_path():
    return _get_rag_child_path('retriever')

def get_rag_retriever_json_path():
    return os.path.join(get_rag_path(), PATH_CONFIG['rag']['retriever']['name'])

def get_temp_path():
    d = os.path.join(BASE_DIR, PATH_CONFIG['temp']['dir'])
    if not os.path.exists(d):
        os.makedirs(d)
    return d
