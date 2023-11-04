import srt
from datetime import timedelta

# Function to adjust (advance or delay) subtitles in an SRT file


def adjust_subtitles(input_file, output_file, time_adjustment_seconds):
    try:
        # Read the original subtitle file
        with open(input_file, 'r', encoding='utf-8') as file:
            original_subs = list(srt.parse(file.read()))

        # Apply the time adjustment to each subtitle
        adjusted_subs = []
        for subtitle in original_subs:
            start_time = subtitle.start + \
                timedelta(seconds=time_adjustment_seconds)
            end_time = subtitle.end + \
                timedelta(seconds=time_adjustment_seconds)
            adjusted_subs.append(srt.Subtitle(
                subtitle.index, start_time, end_time, subtitle.content))

        # Write the adjusted subtitles to the output file
        with open(output_file, 'w', encoding='utf-8') as file:
            file.write(srt.compose(adjusted_subs))

        print(
            f"Subtitles adjusted by {time_adjustment_seconds} seconds and saved to {output_file}")

    except Exception as e:
        print(f"An error occurred: {e}")


# Usage example
if __name__ == "__main__":
    # Replace with the path to your input subtitle file
    input_file = "fresh.off.the.boat.1e04.dvdrip.x264-reward.srt"
    output_file = "output.srt"  # Replace with the desired output file path
    # Adjust this to the number of seconds you want to adjust the subtitles (negative for early, positive for delay)
    time_adjustment_seconds = -1

    adjust_subtitles(input_file, output_file, time_adjustment_seconds)
