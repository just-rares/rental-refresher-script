import os
import tkinter as tk
import time
import re
import subprocess
import threading
import sys

should_stop = False  # Initialize it here
run_script_process = subprocess

def sound_alert(x):
    for _ in range(1, x):
        os.system('echo -e "\a"')
        time.sleep(0.1)


def get_refresh_count(array):
    return len(array)


class LogParsingException(Exception):
    pass


def parse_log_file(file_path, refresh_count_label, room_count_label):
    global should_stop  # Declare 'should_stop' as global

    refreshes = []
    last_line_number = 0

    try:
        while not should_stop:
            result = subprocess.run(["tail", "-n", "+{}".format(last_line_number + 1), file_path], capture_output=True,
                                    text=True)

            lines = result.stdout.splitlines()

            for line in lines:
                if re.search("Error:", line):
                    raise LogParsingException("Found Error. Please check the logs. Remove the errors when done")
                match = re.search(r'#(\d+) \| curr_num: (\d+) \| last_refresh: (\d+:\d+:\d+)', line)
                if match:
                    refresh_number = match.group(1)
                    room_number = match.group(2)
                    refresh_time = match.group(3)
                    refreshes.append((refresh_number, room_number, refresh_time))

            if lines:
                last_line_number += len(lines)

            refresh_count = get_refresh_count(refreshes)
            room_count = refreshes[-1][1] if refreshes else ""
            refresh_count_label.config(text=str(refresh_count))
            room_count_label.config(text=str(room_count))

            time.sleep(0.3)

    except LogParsingException as e:
        print(e)
        sound_alert(50)
        os._exit(1)

def run_script():
    global run_script_process
    run_script_process = subprocess.Popen(["python3", "page-refresher.py"])  # use Popen instead of run


def cleanup(log_thread):
    global run_script_process, should_stop
    print("Program interrupted by user.")
    should_stop = True
    log_thread.join()
    run_script_process.terminate()
    sys.exit(0)


def main():
    thread1 = threading.Thread(target=run_script)
    thread1.start()
    time.sleep(3)
    global should_stop
    file_path = "log.txt"
    should_stop = False

    window = tk.Tk()
    window.title("Room Checker")
    window.geometry("300x120")
    window.protocol("WM_DELETE_WINDOW", lambda: cleanup(log_thread))

    frame = tk.Frame(window)
    frame.pack(pady=20)

    refresh_count_label = tk.Label(frame, text="Number of refreshes:")
    refresh_count_label.grid(column=0, row=0)

    refresh_count_value = tk.Label(frame, text="")
    refresh_count_value.grid(column=1, row=0)

    room_count_label = tk.Label(frame, text="Number of rooms:")
    room_count_label.grid(column=0, row=1)

    room_count_value = tk.Label(frame, text="")
    room_count_value.grid(column=1, row=1)

    button = tk.Button(frame, text="Open Link", command=open_link)
    button.grid(columnspan=2, row=2)

    # Start a separate thread for parsing log file and updating GUI
    log_thread = threading.Thread(target=parse_log_file, args=(file_path, refresh_count_value, room_count_value))
    log_thread.start()

    try:
        window.mainloop()
    except KeyboardInterrupt:
        cleanup(log_thread)






def open_link():
    os.system(f"xdg-open https://5huizenvastgoedbeheer.nl/#/student-housing/")


if __name__ == "__main__":
    try:
        main()
    except Exception:
        print("Program interrupted. some error, idk")
