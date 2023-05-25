from utils import get_last_7_days, get_log_date
from utils import save_dict_to_file, load_dict_from_file
from process_daily_log import process_daily_log
import os
import heapq


def process_7days_logs(log_path, date):
    logs = get_last_7_days(log_path)
    path_storage = "tmp_storage"

    for log in logs:
        date = get_log_date(log)
        country, users = process_daily_log(log)
        save_dict_to_file(country, path_storage + "/country_data", date)
        save_dict_to_file(users, path_storage + "/user_data", date)

        del country
        del users

    process_top_song("country_data", "country", date)
    process_top_song("user_data", "user", date)


def process_top_song(dir, type, date):
    data = os.listdir(dir)
    data.sort()
    final_dict = {}

    for file in data:
        loaded_dict = load_dict_from_file(dir + "/" + file)

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

    top_songs_dict = {}
    for key, songs in final_dict.items():
        top_songs = heapq.nlargest(50, songs, key=songs.get)
        top_songs_dict[key] = {song: songs[song] for song in top_songs}

    with open(type + "_top50_" + date + ".txt", "w") as file:
        for key, songs in top_songs_dict.items():
            song_list = []
            for song, listens in songs.items():
                song_list.append(f"{song}:{listens}")
            song_string = ",".join(song_list)
            file.write(f"{key}|{song_string}\n")
