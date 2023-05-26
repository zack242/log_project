import os
from dotenv import load_dotenv
import heapq
from utils import get_last_7_days, get_log_date, save_dict_to_file, load_dict_from_file
from process_daily_log import process_daily_log

# Load environment variables from .env file
load_dotenv()


""" 
    This function processes the last 7 days of logs and saves the results in a temporary directory.
    It then calls the process_top_song function to process the top 50 songs for each country and user.
    The results are saved in the results directory.
    input: log_path (string) - the path to the log files
    output: None
"""


def process_7days_logs(log_path=os.environ.get("PATH_LOGS")):
    logs = get_last_7_days(log_path)
    path_storage = "tmp_storage"

    for log in logs:
        date = get_log_date(log)

        # Create the directories if they don't exist
        os.makedirs(path_storage + "/country_data", exist_ok=True)
        os.makedirs(path_storage + "/user_data", exist_ok=True)

        # Skip processing if data for the date already exists
        if not os.path.exists(
            path_storage + "/country_data/" + date
        ) and not os.path.exists(path_storage + "/user_data/" + date):
            country, users = process_daily_log(log)
            save_dict_to_file(country, path_storage + "/country_data", date)
            save_dict_to_file(users, path_storage + "/user_data", date)

            # Free memory
            del country
            del users

    date_to_process = get_log_date(logs[0])

    process_top_song(path_storage + "/country_data", "country", date_to_process)
    process_top_song(path_storage + "/user_data", "user", date_to_process)


def process_top_song(dir, type, date):
    filesnames = os.listdir(dir)
    filesnames.sort()
    final_dict = {}

    # only keep the last 7 days of filenames
    filesnames = filesnames[-7:]

    for file in filesnames:
        loaded_dict = load_dict_from_file(os.path.join(dir, file))

        # Iterate over each user in the loaded_dict
        for key, songs in loaded_dict.items():
            if key not in final_dict:
                final_dict[key] = {}

            # Iterate over each song in the current country's dictionary
            for song, listens in songs.items():
                if song in final_dict[key]:
                    final_dict[key][song] += listens
                else:
                    final_dict[key][song] = listens

    path_results = os.environ.get("PATH_RESULTS")

    # Create the directories if they don't exist
    os.makedirs(path_results + type, exist_ok=True)

    with open(
        os.path.join(path_results, type, f"{type}_top50_{date}.txt"), "w"
    ) as file:
        for key, songs in final_dict.items():
            top_songs = heapq.nlargest(50, songs, key=songs.get)
            top_songs_dict = {song: songs[song] for song in top_songs}

            song_list = [
                f"{song}:{listens}" for song, listens in top_songs_dict.items()
            ]
            song_string = ",".join(song_list)
            file.write(f"{key}|{song_string}\n")

    del final_dict
    del top_songs_dict


if __name__ == "__main__":
    process_7days_logs()
