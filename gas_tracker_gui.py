import requests
import json
import os
import time
import datetime
import tkinter as tk
from tkinter import messagebox

DATA_FILE = "gas_history.json"

def get_gas_data():
    try:
        # Menggunakan API publik ethgas.watch
        url = "https://ethgas.watch/api/gas"
        res = requests.get(url)
        data = res.json()

        gas = {
            "timestamp": int(time.time()),
            "SafeGasPrice": int(data["safe"]["maxFee"]),
            "ProposeGasPrice": int(data["normal"]["maxFee"]),
            "FastGasPrice": int(data["fast"]["maxFee"]),
        }
        return gas

    except Exception as e:
        messagebox.showerror("Error", f"Failed to fetch gas data:\n{e}")
        return None

def save_gas_data(entry):
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, "w") as f:
            json.dump([entry], f, indent=2)
    else:
        with open(DATA_FILE, "r+") as f:
            data = json.load(f)
            data.append(entry)
            f.seek(0)
            json.dump(data, f, indent=2)

def view_summary():
    if not os.path.exists(DATA_FILE):
        return "📭 No gas history found."

    with open(DATA_FILE, "r") as f:
        data = json.load(f)

    if not data:
        return "📭 No entries yet."

    avg_safe = sum(d["SafeGasPrice"] for d in data) / len(data)
    avg_propose = sum(d["ProposeGasPrice"] for d in data) / len(data)
    avg_fast = sum(d["FastGasPrice"] for d in data) / len(data)

    return (f"📊 Average Gas Prices (Gwei):\n"
            f"🟢 Safe: {avg_safe:.2f}\n"
            f"🟡 Propose: {avg_propose:.2f}\n"
            f"🔴 Fast: {avg_fast:.2f}")

def fetch_and_display():
    gas = get_gas_data()
    if gas:
        ts = datetime.datetime.fromtimestamp(gas["timestamp"]).strftime('%Y-%m-%d %H:%M:%S')
        output = (f"⏱ {ts}\n"
                  f"🟢 Safe: {gas['SafeGasPrice']} Gwei\n"
                  f"🟡 Propose: {gas['ProposeGasPrice']} Gwei\n"
                  f"🔴 Fast: {gas['FastGasPrice']} Gwei")
        text_output.set(output)
        save_gas_data(gas)

def show_summary_gui():
    summary = view_summary()
    text_output.set(summary)

# GUI Setup
app = tk.Tk()
app.title("ETH Gas Tracker GUI ⛽")
app.geometry("400x300")
app.resizable(False, False)

text_output = tk.StringVar()
text_output.set("Click a button to start.")

label = tk.Label(app, textvariable=text_output, justify="left", font=("Courier", 10), wraplength=380)
label.pack(pady=20)

btn_fetch = tk.Button(app, text="Fetch Latest Gas Price", command=fetch_and_display)
btn_fetch.pack(pady=5)

btn_summary = tk.Button(app, text="Show Gas Summary", command=show_summary_gui)
btn_summary.pack(pady=5)

btn_quit = tk.Button(app, text="Exit", command=app.quit)
btn_quit.pack(pady=20)

app.mainloop()
