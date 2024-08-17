import os


def get_log_file_path():
    log_dir = os.path.join(os.path.expanduser('~'), 'pantalone', 'logs')
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    return log_dir
