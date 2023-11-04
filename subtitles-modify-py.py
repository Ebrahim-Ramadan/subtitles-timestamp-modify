import srt
import tkinter as tk
from datetime import timedelta

root = tk.Tk()
root.title("Subtitles Timestamp Modify")

entry = tk.Entry(root)
entry.pack()


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

    except Exception as e:
        print(f"An error occurred: {e}")


def get_time_adjustment_and_adjust():
    time_adjustment_str = entry.get()

    if is_not_number(time_adjustment_str):
        print("Invalid input. Please enter a valid number.")
    else:
        time_adjustment_seconds = float(time_adjustment_str)

        input_file = "fresh.off.the.boat.1e04.dvdrip.x264-reward.srt"
        output_file = "output.srt"
        adjust_subtitles(input_file, output_file, time_adjustment_seconds)


adjust_button = tk.Button(root, text="Adjust Subtitles",
                          command=get_time_adjustment_and_adjust)
adjust_button.pack()

root.mainloop()
