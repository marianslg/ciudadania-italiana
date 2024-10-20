import sys
from main import start_process_7, start_process_day

if __name__ == '__main__':
    if len(sys.argv) > 1:
        if sys.argv[1] == "7":
            start_process_7()
        elif sys.argv[1] == "day":
            start_process_day()
    else:
        print("Run with 'python index.py 7' or 'python index.py day'")