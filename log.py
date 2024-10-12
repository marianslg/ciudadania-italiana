import os

LOG_FOLDER = 'logs'

def save_log(message, log_file=f'{LOG_FOLDER}/log.txt'):
    from datetime import datetime

    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    message = f"{current_time} - {message}"
    print(message)

    create_folder_if_not_exists('logs')

    with open(log_file, 'a') as file:
        file.write(f"{message}\n")


def save_file(file_name, content):
    with open(file_name, 'w') as file:
        file.write(content)


def create_folder_if_not_exists(screenshot_url):
    if not os.path.exists(screenshot_url):
        os.makedirs(screenshot_url)
