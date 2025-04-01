import os
import asyncio
import psutil
from playwright.async_api import async_playwright
import tkinter as tk
from tkinter import ttk
from datetime import datetime, timedelta
import time
import pyautogui
import requests
import json
import threading

# Telegram configuration - sensitive data replaced
TELEGRAM_BOT_TOKEN = "***"
TELEGRAM_CHAT_ID = "***"

# Declare global variables
global first_break_after_var, first_break_duration_var, lunch_after_var, lunch_duration_var
global second_break_after_var, second_break_duration_var, close_after_var, total_time_label
global schedule_hour_var, schedule_minute_var, start_on_shift_var, root


def close_chrome_processes():
    for process in psutil.process_iter(['name']):
        if 'chrome' in process.info['name'].lower():
            try:
                process.kill()
                print(f"Chrome process with PID {process.pid} terminated.")
            except Exception as e:
                print(f"Failed to terminate process: {e}")


async def delay(seconds):
    await asyncio.sleep(seconds)


async def set_status(page, status):
    if status == "Ready":
        await page.keyboard.press('ArrowDown')
        await page.keyboard.press('ArrowDown')
        await page.keyboard.press('Enter')
        print("Status set to Ready")
        await delay(2)
        send_screenshot_notification("Status updated to Ready")
    elif status == "Break":
        await page.keyboard.press('ArrowDown')
        await page.keyboard.press('ArrowDown')
        await page.keyboard.press('ArrowDown')
        await page.keyboard.press('Enter')
        print("Status set to Break")
        await delay(1)
        send_screenshot_notification("Status set to Break")
    elif status == "Lunch":
        for _ in range(6):
            await page.keyboard.press('ArrowDown')
        await page.keyboard.press('Enter')
        print("Status set to Lunch")
        await delay(1)
        send_screenshot_notification("Status set to Lunch")


async def run_script(first_break_after, first_break_duration, lunch_after, lunch_duration, second_break_after,
                     second_break_duration, close_after, start_on_shift):
    close_chrome_processes()

    try:
        async with async_playwright() as p:
            print("Launching browser...")
            browser = await p.chromium.launch_persistent_context(
                user_data_dir=os.getenv('LOCALAPPDATA') + '\\Google\\Chrome\\User Data',
                headless=False,
                executable_path="C:/Program Files/Google/Chrome/Application/chrome.exe",
                args=['--start-maximized']
            )
            send_telegram_message("Программа началаРаботу!")

            page1 = await browser.new_page()
            await page1.goto("***")  # URL replaced
            print("First tab opened")

            page2 = await browser.new_page()
            await page2.goto("***")  # URL replaced
            print("Second tab opened")

            await delay(5)

            await page2.keyboard.press('Enter')
            await delay(1)
            await page2.keyboard.press('Enter')
            print("Login Enter pressed")

            login_attempts = 0
            max_attempts = 8

            while True:
                try:
                    await page2.wait_for_function(
                        "document.querySelector('body').innerText.includes('Ready')", timeout=5000
                    )
                    print("Login successful.")
                    await delay(2)
                    send_screenshot_notification("Successful Login")

                    # Start on shift delay
                    await delay(int(start_on_shift))

                    break
                except Exception:
                    login_attempts += 1
                    print(f"Login failed, retrying in 5 seconds... (Attempt {login_attempts})")
                    await delay(5)
                    if login_attempts >= max_attempts:
                        send_telegram_message(
                            "🚨 Внимание! 🚨\n\nПопытки входа в систему неудачны. Проверьте данные для входа и состояние сервиса. 🔴"
                        )
                        break

            if login_attempts < max_attempts:
                await set_status(page2, "Ready")

            await delay(int(first_break_after))
            await set_status(page2, "Break")

            await delay(int(first_break_duration))
            await set_status(page2, "Ready")

            await delay(int(lunch_after))
            await set_status(page2, "Lunch")

            await delay(int(lunch_duration))
            await set_status(page2, "Ready")

            await delay(int(second_break_after))
            await set_status(page2, "Break")

            await delay(int(second_break_duration))
            await set_status(page2, "Ready")

            await delay(int(close_after))
            print("Script completion")

    except Exception as e:
        print(f"Error during script execution: {e}")
        send_error_notification(f"Ошибка во время работы: {e}")
    finally:
        if browser:
            print("Closing browser...")
            try:
                await browser.close()
            except Exception as e:
                print(f"Failed to close browser: {e}")
        send_telegram_message("Программа завершилаРаботу!")
        print("Script completed.")


def send_telegram_message(message):
    url = f"***"  # URL replaced
    params = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "Markdown"
    }
    try:
        response = requests.post(url, params=params, timeout=10)
        response.raise_for_status()
        print("Telegram message sent successfully.")
    except requests.exceptions.RequestException as e:
        print(f"Failed to send Telegram message: {e}")


def send_telegram_photo(photo_path):
    url = f"***"  # URL replaced
    try:
        with open(photo_path, "rb") as file:
            files = {"photo": file}
            data = {"chat_id": TELEGRAM_CHAT_ID}
            response = requests.post(url, data=data, files=files, timeout=30)
            response.raise_for_status()
            print("Telegram photo sent successfully.")
    except requests.exceptions.RequestException as e:
        print(f"Failed to send Telegram photo: {e}")

def send_telegram_file(file_path):
    url = f"***"  # URL replaced
    try:
        with open(file_path, "rb") as file:
            files = {"document": file}
            data = {"chat_id": TELEGRAM_CHAT_ID}
            response = requests.post(url, data=data, files=files, timeout=30)
            response.raise_for_status()
            print("Telegram file sent successfully.")
    except requests.exceptions.RequestException as e:
        print(f"Failed to send Telegram file: {e}")

def take_screenshot():
    screenshot = pyautogui.screenshot()
    screenshot_path = "screenshot.png"
    try:
        screenshot.save(screenshot_path)
        return screenshot_path
    except Exception as e:
        print(f"Error capturing screenshot: {e}")

def send_screenshot_notification(message):
    screenshot_path = take_screenshot()
    if screenshot_path:
        send_telegram_message(message)
        send_telegram_file(screenshot_path)
    else:
        send_telegram_message(f"{message} (No screenshot available)")


def send_error_notification(error_message):
    send_screenshot_notification(error_message)


def test_program():
    asyncio.run(run_script(
        int(first_break_after_var.get()),
        int(first_break_duration_var.get()),
        int(lunch_after_var.get()),
        int(lunch_duration_var.get()),
        int(second_break_after_var.get()),
        int(second_break_duration_var.get()),
        int(close_after_var.get()),
        int(start_on_shift_var.get())
    ))


def update_total_time(*args):
    try:
        total = sum([
            float(first_break_after_var.get()),
            float(first_break_duration_var.get()),
            float(lunch_after_var.get()),
            float(lunch_duration_var.get()),
            float(second_break_after_var.get()),
            float(second_break_duration_var.get()),
            float(close_after_var.get())
        ])

        hours = int(total // 3600)
        minutes = int((total % 3600) // 60)
        seconds = int(total % 60)
        total_time_label.config(text=f"Total Time: {total:.0f} sec ({hours}h {minutes}m {seconds}s)")
    except ValueError:
        total_time_label.config(text="Error in input values")


def start_program_at_scheduled_time(root):
    try:
        schedule_hour = int(schedule_hour_var.get())
        schedule_minute = int(schedule_minute_var.get())

        current_time = datetime.now()
        target_time = current_time.replace(hour=schedule_hour, minute=schedule_minute, second=0, microsecond=0)

        if target_time < current_time:
            target_time += timedelta(days=1)

        delay_seconds = (target_time - current_time).total_seconds()
        delay_timedelta = timedelta(seconds=delay_seconds)
        delay_str = str(delay_timedelta).split('.')[0]

        scheduled_time_str = f"{schedule_hour:02d}:{schedule_minute:02d}"
        message = f"Начало работы запланировано на {scheduled_time_str} через {delay_str}"

        send_telegram_message(message)

        delay_ms = int(delay_seconds * 1000)

        root.after(delay_ms, lambda: asyncio.run(run_script(
            int(first_break_after_var.get()),
            int(first_break_duration_var.get()),
            int(lunch_after_var.get()),
            int(lunch_duration_var.get()),
            int(second_break_after_var.get()),
            int(second_break_duration_var.get()),
            int(close_after_var.get()),
            int(start_on_shift_var.get())
        )))
    except Exception as e:
        send_telegram_message(f"Ошибка расписания: {e}")


def create_interface():
    global first_break_after_var, first_break_duration_var, lunch_after_var, lunch_duration_var
    global second_break_after_var, second_break_duration_var, close_after_var, total_time_label
    global schedule_hour_var, schedule_minute_var, start_on_shift_var, root

    root = tk.Tk()
    root.title("Task Scheduler")
    root.geometry("315x500")
    root.configure(bg='#f0f0f0')

    style = ttk.Style()
    style.theme_use('clam')
    style.configure('TFrame', background='#f0f0f0')
    style.configure('TLabel', background='#f0f0f0', font=('Arial', 9))
    style.configure('TEntry', font=('Arial', 9))
    style.configure('TButton', font=('Arial', 9), padding=5)
    style.configure('TotalTime.TLabel', font=('Arial', 11, 'bold'))

    current_time = datetime.now()
    schedule_hour_var = tk.StringVar(value=f"{current_time.hour:02d}")
    schedule_minute_var = tk.StringVar(value=f"{current_time.minute:02d}")
    start_on_shift_var = tk.StringVar(value="180")

    first_break_after_var = tk.StringVar(value="7200")
    first_break_duration_var = tk.StringVar(value="899")
    lunch_after_var = tk.StringVar(value="4500")
    lunch_duration_var = tk.StringVar(value="1799")
    second_break_after_var = tk.StringVar(value="9000")
    second_break_duration_var = tk.StringVar(value="899")
    close_after_var = tk.StringVar(value="6404")

    first_break_after_var.trace("w", update_total_time)
    first_break_duration_var.trace("w", update_total_time)
    lunch_after_var.trace("w", update_total_time)
    lunch_duration_var.trace("w", update_total_time)
    second_break_after_var.trace("w", update_total_time)
    second_break_duration_var.trace("w", update_total_time)
    close_after_var.trace("w", update_total_time)

    schedule_frame = ttk.Frame(root, padding=8)
    schedule_frame.grid(row=0, column=0, columnspan=2, pady=8, sticky='nsew')

    tk.Label(schedule_frame, text="Schedule Time (hh:mm):", bg='#f0f0f0').grid(row=0, column=0, pady=5)
    schedule_hour_entry = ttk.Combobox(schedule_frame, textvariable=schedule_hour_var,
                                       values=[f"{i:02d}" for i in range(24)], width=5)
    schedule_hour_entry.grid(row=0, column=1, pady=5)
    schedule_minute_entry = ttk.Combobox(schedule_frame, textvariable=schedule_minute_var,
                                         values=[f"{i:02d}" for i in range(60)], width=5)
    schedule_minute_entry.grid(row=0, column=2, pady=5)

    input_frame = ttk.Frame(root, padding=8)
    input_frame.grid(row=1, column=0, columnspan=2, pady=8, sticky='nsew')

    entries = [
        ("First Break After (sec):", first_break_after_var),
        ("First Break Duration (sec):", first_break_duration_var),
        ("Lunch After (sec):", lunch_after_var),
        ("Lunch Duration (sec):", lunch_duration_var),
        ("Second Break After (sec):", second_break_after_var),
        ("Second Break Duration (sec):", second_break_duration_var),
        ("Close After (sec):", close_after_var),
        ("Start on Shift (sec):", start_on_shift_var)
    ]
    for idx, (label, var) in enumerate(entries):
        tk.Label(input_frame, text=label, bg='#f0f0f0').grid(row=idx, column=0, pady=5)
        entry = ttk.Entry(input_frame, textvariable=var, width=10)
        entry.grid(row=idx, column=1, pady=5)

    button_frame = ttk.Frame(root, padding=8)
    button_frame.grid(row=2, column=0, columnspan=2, pady=8, sticky='nsew')

    start_button = ttk.Button(button_frame, text="Start", command=lambda: start_program_at_scheduled_time(root))
    start_button.grid(row=0, column=0, padx=5)

    test_button = ttk.Button(button_frame, text="Test", command=test_program)
    test_button.grid(row=0, column=1, padx=5)

    total_time_label = ttk.Label(root, text="Total Time: Calculating...", style='TotalTime.TLabel')
    total_time_label.grid(row=3, column=0, columnspan=2, pady=8)

    update_total_time()

    root.mainloop()


def send_welcome_message():
    url = f"***"  # URL replaced

    params = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": "Welcome to the bot!"
    }
    requests.post(url, params=params)

    keyboard = {
        "inline_keyboard": [
            [
                {
                    "text": "Check Status",
                    "callback_data": "check_status"
                }
            ]
        ]
    }
    params = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": "Check Status",
        "reply_markup": json.dumps(keyboard)
    }
    requests.post(url, params=params)


def process_telegram_updates():
    offset = 0
    while True:
        try:
            url = f"***"  # URL replaced
            params = {
                "offset": offset,
                "timeout": 10
            }
            response = requests.get(url, params=params, timeout=30)
            response.raise_for_status()
            updates = response.json()
            if updates.get("ok") and updates.get("result"):
                for update in updates["result"]:
                    if "callback_query" in update:
                        query = update["callback_query"]
                        if query.get("data") == "check_status":
                            send_screenshot_notification("Status check requested")
                            url = f"***"  # URL replaced
                            requests.get(url, params={"callback_query_id": query["id"]})
                    offset = max(offset, update["update_id"] + 1)
        except (requests.exceptions.RequestException, KeyError, ValueError) as e:
            print(f"Error processing Telegram updates: {e}")
        time.sleep(1)


telegram_thread = threading.Thread(target=process_telegram_updates)
telegram_thread.daemon = True
telegram_thread.start()

send_welcome_message()

if __name__ == "__main__":
    create_interface()