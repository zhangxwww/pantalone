import os


def get_log_file_path():
    log_dir = os.path.join(os.path.expanduser('~'), 'pantalone', 'logs')
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    return log_dir


def get_db_path():
    db_dir = os.path.join(os.path.expanduser('~'), 'pantalone', 'db')
    if not os.path.exists(db_dir):
        os.makedirs(db_dir)
    return os.path.join(db_dir, 'pantalone.db')
