import os
import tkinter as tk
import time
import re
import subprocess
import threading
import sys
import page_refresher

should_stop = False  # Initialize it here
run_script_process = subprocess
running = True

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
        page_refresher.sound_alert(50)
        os._exit(1)


def run_script():
    global run_script_process
    run_script_process = subprocess.Popen(["python3", "page_refresher.py"])  # use Popen instead of run


def cleanup(log_thread, countdown_thread):
    global run_script_process, should_stop
    print("Program interrupted by user.")
    page_refresher.log(f"gui - Program stopped at time {time.strftime('%H:%M:%S')}")
    should_stop = True
    log_thread.join()
    countdown_thread.join()
    run_script_process.terminate()
    os.system("kill python")
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
    window.geometry("300x160")

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

    refresh_rate_label = tk.Label(frame, text="Refresh Rate:")
    refresh_rate_label.grid(column=0, row=2)

    refresh_rate_value = tk.Label(frame, text=str(int(page_refresher.set_refresh_rate() / 60)) + "m")
    refresh_rate_value.grid(column=1, row=2)
    global countdown_label
    countdown_label = tk.Label(frame, text="")
    countdown_label.grid(columnspan=2, row=3)
    countdown_thread = threading.Thread(target=countdown,
                                        args=(countdown_label,
                                              page_refresher.set_refresh_rate()))

    countdown_thread.start()

    button = tk.Button(frame, text="Open Link", command=open_link)
    button.grid(columnspan=2, row=4)

    log_thread = threading.Thread(target=parse_log_file, args=(file_path, refresh_count_value, room_count_value))
    log_thread.start()
    window.protocol("WM_DELETE_WINDOW", lambda: cleanup(log_thread, countdown_thread))
    try:
        window.mainloop()
    except KeyboardInterrupt:
        cleanup(log_thread, countdown_thread)

def countdown(label, seconds):
    global running
    while seconds >= 0 and running:
        minutes, sec = divmod(seconds, 60)
        label.config(text=f"{minutes:02d}:{sec:02d}")
        time.sleep(1)
        seconds -= 1


def open_link():
    os.system(f"xdg-open https://5huizenvastgoedbeheer.nl/#/student-housing/")


if __name__ == "__main__":
    try:
        main()
    except Exception:
        print("Program interrupted. some error, idk")
