from decorators import create_folder, create_folder_if_not_exists
import pandas as pd

LOG_FOLDER = 'logs'
LOG_FILE = f'{LOG_FOLDER}/log.txt'
RESULT_FILE = f'{LOG_FOLDER}/result.csv'

@create_folder(LOG_FOLDER)
def save_log(message):
    from datetime import datetime

    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    message = f"{current_time} - {message}"
    
    # print(message)

    create_folder_if_not_exists('logs')

    with open(LOG_FILE, 'a') as file:
        file.write(f"{message}\n")


def save_file(file_name, content):
    with open(file_name, 'w') as file:
        file.write(content)


@create_folder(LOG_FOLDER)
def save_result_operation(date, hour, result):
    with open(RESULT_FILE, 'a') as file:
        file.write(f"{date},{hour},{result}\n")

def get_result_operation():
    # Cargar los datos desde el CSV
    df = pd.read_csv(RESULT_FILE, header=None)

    # Asignar nombres a las columnas manualmente
    df.columns = ["fecha", "hora", "resultado"]

    # Contar cantidad total de resultados
    cantidad_total = len(df)

    # Contar cantidad de resultados "OK" y "FAIL"
    cantidad_ok = df[df["resultado"] == "OK"].shape[0]
    cantidad_fail = df[df["resultado"] == "FAIL"].shape[0]
    cantidad_none = df[df["resultado"] == "NONE"].shape[0]

    # Obtener la última fecha y hora registrada
    ultima_fila = df.iloc[-1]
    ultima_fecha = ultima_fila["fecha"]
    ultima_hora = ultima_fila["hora"]

    return f'TOTAL: {cantidad_total}. OK: {cantidad_ok}. FAIL: {cantidad_fail}. NONE: {cantidad_none}. Última fecha: {ultima_fecha} {ultima_hora}'