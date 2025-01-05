import json
from process import Process
from datetime import datetime
import threading



milliseconds = [200000, 300000, 400000, 500000]
# milliseconds = [200000]

if __name__ == "__main__":
  threads = []

  for ms in milliseconds:
    execution_time = datetime.now().replace(hour=18, minute=59, second=59, microsecond=ms)
    process = Process(f'P{ms}', execution_time)
    thread = threading.Thread(target=process.run)
    thread.start()
    threads.append(thread)
  
  # Asegurarse de que cada hilo termine y libere los recursos
  for thread in threads:
    thread.join()
