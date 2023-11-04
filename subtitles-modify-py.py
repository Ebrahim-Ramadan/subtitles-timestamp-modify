import srt
import tkinter as tk
from datetime import timedelta
from tkinter import filedialog
import os

root = tk.Tk()
root.title("Subtitles Timestamp Modify")
root.geometry('400x100')


def is_not_number(input_str):
    try:
        float(input_str)
    except ValueError:
        return True
    return False


def adjust_subtitles(input_file, output_file, time_adjustment_seconds):
    try:
        with open(input_file, 'r', encoding='utf-8') as file:
            original_subs = list(srt.parse(file.read()))

        adjusted_subs = []
        for subtitle in original_subs:
            start_time = subtitle.start + \
                timedelta(seconds=time_adjustment_seconds)
            end_time = subtitle.end + \
                timedelta(seconds=time_adjustment_seconds)
            adjusted_subs.append(srt.Subtitle(
                subtitle.index, start_time, end_time, subtitle.content))

        with open(output_file, 'w', encoding='utf-8') as file:
            file.write(srt.compose(adjusted_subs))

        print(
            f"Subtitles adjusted by {time_adjustment_seconds} seconds and saved to {output_file}")
        timeEntry.delete(0, tk.END)
    except Exception as e:
        print(f"An error occurred: {e}")


def srt_file_browsing():
    global input_file
    input_file = filedialog.askopenfilename(
        filetypes=[("SRT files", "*.srt")])
    if (input_file):

        input_file_name = os.path.basename(input_file)
        fileName_Label.config(text=input_file_name)
        return input_file
    return False


def get_time_adjustment_and_adjust():
    time_adjustment_str = timeEntry.get()

    if is_not_number(time_adjustment_str):
        print("Invalid input. Please enter a valid number.")
    else:
        time_adjustment_seconds = float(time_adjustment_str)

        if input_file:
            output_file = filedialog.asksaveasfilename(
                defaultextension=".srt", filetypes=[("SRT files", "*.srt")])

            if output_file:
                adjust_subtitles(input_file, output_file,
                                 time_adjustment_seconds)


Browsebtn = tk.Button(root, text="Browse srt file",
                      command=srt_file_browsing)
Browsebtn.pack()
fileName_Label = tk.Label(root, text='')
fileName_Label.pack()

timeEntry = tk.Entry(root)
timeEntry.pack()

adjust_button = tk.Button(root, text="Adjust and save",
                          command=get_time_adjustment_and_adjust)
adjust_button.pack()

root.mainloop()
