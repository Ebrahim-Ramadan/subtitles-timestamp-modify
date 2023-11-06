import srt
import tkinter as tk
from datetime import timedelta
from tkinter import filedialog
import os
import glob

root = tk.Tk()
root.title("Subtitles Timestamp Modify")
root.geometry('400x400')


def show_error_message(message):
    error_window = tk.Toplevel()
    error_window.title("Error")

    label = tk.Label(error_window, text=message, padx=10, pady=10)
    label.pack()

    ok_button = tk.Button(error_window, text="OK",
                          command=error_window.destroy)
    ok_button.pack()


def is_not_number(input_str):
    try:
        float(input_str)
    except ValueError:
        return True
    return False


def open_and_display_srt(input_file, *args, **kwargs):
    try:
        with open(input_file, 'r', encoding='utf-8') as srt_file:
            content = srt_file.read()
            read_window = tk.Toplevel(root)
            read_window.title(f"{input_file} content")
            read_window.geometry("300x200")
            text_widget = tk.Text(read_window, wrap="none")
            text_widget.insert("1.0", content)
            text_widget.pack(fill="both", expand=True)
    except FileNotFoundError:
        print(f"The file '{input_file}' was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")


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
        show_error_message(e)
        raise ValueError("An error occurred:", e)


input_file = None


def srt_file_browsing():
    global input_file
    input_file = filedialog.askopenfilename(
        filetypes=[("SRT files", "*.srt")])
    if (input_file):
        input_file_name = os.path.basename(input_file)
        fileName_Label.config(text=input_file_name)
        return input_file
    return False


def srt_folder_browsing():
    global folderPath, srt_files
    DIR_label = tk.Label(root, text='', wraplength=400)
    folderPath = filedialog.askdirectory(title="Select a folder")
    if folderPath:
        srt_files = glob.glob(os.path.join(folderPath, '*.srt'))

        if srt_files:
            for single_srt_file in srt_files:
                input_file_name = os.path.basename(single_srt_file)
                display_button = tk.Button(
                    root, text=f"Display {input_file_name}", command=lambda file=single_srt_file: open_and_display_srt(file))
                display_button.pack()

        else:
            DIR_label.config(text='no .srt files found')
    else:
        show_error_message('error found in the chosen directory')


def get_time_adjustment_and_adjust():
    time_adjustment_str = timeEntry.get()

    if is_not_number(time_adjustment_str):
        show_error_message("Invalid input. Please enter a valid number.")
        raise ValueError("Invalid input. Please enter a valid number.")
    else:
        time_adjustment_seconds = float(time_adjustment_str)

        if input_file:
            output_file = filedialog.asksaveasfilename(
                defaultextension=".srt", filetypes=[("SRT files", "*.srt")])

            if output_file:
                adjust_subtitles(input_file, output_file,
                                 time_adjustment_seconds)
        elif srt_files:
            folder_output = filedialog.askdirectory()
            for single_srt_file in srt_files:
                input_file_name = os.path.basename(single_srt_file)
                output_file = os.path.join(folder_output, input_file_name)
                adjust_subtitles(single_srt_file, output_file,
                                 time_adjustment_seconds)


BrowseFiles_btn = tk.Button(root, text="Browse srt file",
                            command=srt_file_browsing)
BrowseFiles_btn.pack()

fileName_Label = tk.Label(root, text='')
fileName_Label.pack()

BrowseDIR_btn = tk.Button(root, text="select a directory",
                          command=srt_folder_browsing)
BrowseDIR_btn.pack()

timeEntry = tk.Entry(root)
timeEntry.pack()

adjust_button = tk.Button(root, text="Adjust and save",
                          command=get_time_adjustment_and_adjust)
adjust_button.pack()


root.mainloop()
