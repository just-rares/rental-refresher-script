from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
import tkinter as tk
from tkinter import messagebox
import os
from datetime import datetime

WEBSITE_URL = "https://5huizenvastgoedbeheer.nl/#/student-housing/"
TARGET_DIV_SELECTOR = "div.q-chip.text-positive > div.q-chip__content"

chrome_options = Options()
chrome_options.add_argument("--headless")


def set_refresh_rate():
    day = datetime.now().day
    if day < 21:
        return 3600
    if day < 23:
        return 1800
    if day < 25:
        return 600
    return 60



def sound_alert(x):
    for _ in range(1, x):
        os.system('echo -e "\a"')
        time.sleep(0.1)


def check_number_change(previous_number, current_number):
    if previous_number != current_number:
        msg = f"Number has changed! Previous: {previous_number}, Current: {current_number}"
        log(msg)
        messagebox.showinfo("Room Found", "The number changed. There may be rooms available")
        sound_alert(5000)


def log(msg):
    with open('log.txt', 'a') as f:
        f.write(f"{msg}\n")


def save_count(cnt):
    with open('count.txt', 'w') as f:
        f.write(f"{cnt}")


def load_count():
    try:
        with open('count.txt', 'r') as f:
            return int(f.read().strip())
    except FileNotFoundError:
        return 1


def main():
    refresh_rate = set_refresh_rate()
    root = tk.Tk()
    root.withdraw()
    driver = webdriver.Chrome(options=chrome_options)
    try:
        driver.get(WEBSITE_URL)

        previous_number = None
        cnt = load_count()
        log(f"Program started at time {time.strftime('%H:%M:%S')}")

        print(
            f"Program started successfully.\nCurrent date: {datetime.now()}\nCurrent Refresh Rate: {int(refresh_rate / 60)}m\nCurrent count of refreshes: {cnt - 1}")

        while True:
            driver.refresh()
            time.sleep(2)

            try:
                number_element = driver.find_element(By.CSS_SELECTOR, TARGET_DIV_SELECTOR)
                current_number = int(number_element.text.strip())
                if previous_number is not None:
                    check_number_change(previous_number, current_number)
                previous_number = current_number

            except Exception as e:
                log(f"Error: {str(e)}")
                print(f"Error: {str(e)}")
                messagebox.showinfo("ERROR", "Something went wrong. Please check the log files")

            current_time = time.strftime("%H:%M:%S")
            log(f"#{cnt} | curr_num: {current_number} | last_refresh: {current_time}")

            cnt += 1
            save_count(cnt)
            time.sleep(refresh_rate)

    except Exception as e:
        log(f"Error: {str(e)}")
    finally:
        log(f"Program stopped at time {time.strftime('%H:%M:%S')}")
        print(f"Program stopped at time {time.strftime('%H:%M:%S')}")
        driver.quit()


if __name__ == "__main__":
    try:
        main()
        print(f"Program stopped at time {time.strftime('%H:%M:%S')}")
    except Exception as e:
        log(e)
        print("Program interrupted by user. FILE: page_refresher.py")
