# import threading
# import time
# from selenium import webdriver
# from selenium.webdriver.chrome.service import Service

# # Shared list to hold browser instances
# browsers = []
# list_lock = threading.Lock()

# def browser_thread(sleep_time, index):
#     # Open browser
#     browser = webdriver.Chrome()
    
#     # Append to shared list
#     with list_lock:
#         browsers.append((index, browser))
    
#     # Sleep for specified time
#     time.sleep(sleep_time)
    
#     if index == 4:
#         # This is the fifth browser
#         print(f"Fifth browser (index {index}) waking up after {sleep_time} seconds.")
#         # Wait until all browsers are in the list
#         while True:
#             with list_lock:
#                 if len(browsers) >= 5:
#                     break
#             time.sleep(0.1)
        
#         # Close the first four browsers
#         with list_lock:
#             for idx, br in browsers[:4]:
#                 print(f"Closing browser {idx}.")
#                 br.quit()
#         print("First four browsers have been closed.")
#         print("Fifth browser is still running.")
#         # Keep the fifth browser open indefinitely
#         while True:
#             time.sleep(1)
#     else:
#         print(f"Browser {index} is sleeping for {sleep_time} seconds.")
#         # Keep the browser open until it's closed
#         try:
#             while True:
#                 time.sleep(1)
#         except:
#             pass

# # Create and start threads
# threads = []

# # Start first four threads
# for i in range(4):
#     t = threading.Thread(target=browser_thread, args=(10, i))
#     t.start()
#     threads.append(t)

# # Start fifth thread
# t5 = threading.Thread(target=browser_thread, args=(3, 4))
# t5.start()
# threads.append(t5)

# # Wait for the first four threads to finish
# for t in threads[:-1]:
#     t.join()

# print("Only the fifth browser should be running now.")

import time
import datetime

def ejecutar_en_hora_especifica(funcion, hora_objetivo, *args, **kwargs):
    # hora_objetivo debe ser un timestamp en segundos (desde la época Unix)
    tiempo_actual = time.time()
    retraso = hora_objetivo - tiempo_actual
    if retraso > 0:
        time.sleep(retraso)
    funcion(*args, **kwargs)

def mi_funcion(hora_objetivo):
    tiempo_ejecucion = time.time()
    formato = "%H:%M:%S.%f"

    # Convertimos la hora objetivo y de ejecución al formato deseado
    hora_objetivo_formateada = datetime.datetime.fromtimestamp(hora_objetivo).strftime(formato)[:-3]
    tiempo_ejecucion_formateada = datetime.datetime.fromtimestamp(tiempo_ejecucion).strftime(formato)[:-3]

    print(f"Hora objetivo: {hora_objetivo_formateada}")
    print(f"Hora de ejecución: {tiempo_ejecucion_formateada}")

# Establece la hora objetivo (por ejemplo, en 5.123 segundos desde ahora)
hora_objetivo = time.time() + 5.123

# Ejecutamos la función en la hora objetivo, pasando la hora objetivo como argumento
ejecutar_en_hora_especifica(mi_funcion, hora_objetivo, hora_objetivo)