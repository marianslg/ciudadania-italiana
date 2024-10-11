def save_log(message, log_file='log.txt'):
    import os
    from datetime import datetime

    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    message=f"{current_time} - {message}"
    print(message)
    with open(log_file, 'a') as file:
        file.write(f"{message}\n")



def save_file(file_name, content):
    with open(file_name, 'w') as file:
        file.write(content)