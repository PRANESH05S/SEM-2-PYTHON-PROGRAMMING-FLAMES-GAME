import tkinter as tk
from tkinter import messagebox
import json
import os

# ---------------- Utility Functions ----------------
def count_common_letters(name1, name2):
    name1_list = list(name1.lower().replace(" ", ""))
    name2_list = list(name2.lower().replace(" ", ""))
    for letter in name1_list[:]:
        if letter in name2_list:
            name1_list.remove(letter)
            name2_list.remove(letter)
    return len(name1_list + name2_list)

def flames_result(count):
    flames = ["Friends", "Loyal", "Affection", "Magnificent", "Enemies", "Sensible"]
    while len(flames) > 1:
        split_index = (count % len(flames)) - 1
        if split_index >= 0:
            right = flames[split_index + 1:]
            left = flames[:split_index]
            flames = right + left
        else:
            flames = flames[:len(flames) - 1]
    return flames[0]

def validate_name(name):
    return name.replace(" ", "").isalpha()

def save_result(name1, name2, result):
    filename = "flames_history.json"
    data = []
    if os.path.exists(filename):
        with open(filename, "r") as f:
            data = json.load(f)
    data.append({"name1": name1, "name2": name2, "result": result})
    with open(filename, "w") as f:
        json.dump(data, f, indent=4)

def show_history():
    filename = "flames_history.json"
    if os.path.exists(filename):
        with open(filename, "r") as f:
            data = json.load(f)
        history_text = ""
        for record in data:
            history_text += f"{record['name1']} + {record['name2']} = {record['result']}\n"
        return history_text
    return "No history found!"

# ---------------- GUI Functions ----------------
def calculate_flames():
    name1 = entry_name1.get().strip()
    name2 = entry_name2.get().strip()
    
    if not validate_name(name1) or not validate_name(name2):
        messagebox.showerror("Invalid Input", "Names must contain only letters and spaces!")
        return
    
    count = count_common_letters(name1, name2)
    result = flames_result(count)
    label_result.config(text=f"💖 Relationship: {result}")
    
    save_result(name1, name2, result)
    text_history.config(state='normal')
    text_history.delete(1.0, tk.END)
    text_history.insert(tk.END, show_history())
    text_history.config(state='disabled')

# ---------------- Main GUI ----------------
root = tk.Tk()
root.title("🌟 FLAMES Game 🌟")
root.geometry("500x600")
root.config(bg="#FFE4E1")

# Title Label
tk.Label(root, text="FLAMES Game", font=("Arial", 24, "bold"), bg="#FFE4E1").pack(pady=20)

# Name Inputs
frame_input = tk.Frame(root, bg="#FFE4E1")
frame_input.pack(pady=10)

tk.Label(frame_input, text="Enter First Name:", font=("Arial", 14), bg="#FFE4E1").grid(row=0, column=0, padx=10, pady=5, sticky='w')
entry_name1 = tk.Entry(frame_input, font=("Arial", 14))
entry_name1.grid(row=0, column=1, padx=10, pady=5)

tk.Label(frame_input, text="Enter Second Name:", font=("Arial", 14), bg="#FFE4E1").grid(row=1, column=0, padx=10, pady=5, sticky='w')
entry_name2 = tk.Entry(frame_input, font=("Arial", 14))
entry_name2.grid(row=1, column=1, padx=10, pady=5)

# Calculate Button
tk.Button(root, text="Calculate FLAMES", font=("Arial", 14, "bold"), bg="#FF69B4", fg="white", command=calculate_flames).pack(pady=20)

# Result Label
label_result = tk.Label(root, text="💖 Relationship: ", font=("Arial", 16, "bold"), bg="#FFE4E1", fg="#FF1493")
label_result.pack(pady=10)

# History Section
tk.Label(root, text="Previous Matches:", font=("Arial", 14, "bold"), bg="#FFE4E1").pack(pady=10)
text_history = tk.Text(root, height=10, width=50, font=("Arial", 12))
text_history.pack(pady=5)
text_history.insert(tk.END, show_history())
text_history.config(state='disabled')

# Run GUI
root.mainloop()
