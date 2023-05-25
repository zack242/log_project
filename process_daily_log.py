import psutil
from collections import defaultdict
from utils import is_country_code


"""
    This function processes a daily log file and returns two dictionaries:
    input: log_files (string) - name of the log file
    output: dict_country (dictionary) - dictionary of countries
"""


def process_daily_log(log_files):
    # We initialize two dictionaries, one for countries and one for users
    dict_country = defaultdict(lambda: defaultdict(int))
    dict_users = defaultdict(lambda: defaultdict(int))

    # We iterate through the log file
    with open("logs/" + log_files, "r") as f:
        lines = f.readlines()
        batch_size = 1_000_000
        num_lines = len(lines)
        num_batches = (num_lines // batch_size) + 1

        # We iterate through the log file in batches of 1 million lines
        for batch in range(num_batches):
            start_index = batch * batch_size
            end_index = min((batch + 1) * batch_size, num_lines)

            for i in range(start_index, end_index):
                tmp = lines[i].split("|")

                # We remove the newline character from the last element and check if the log line is valid
                if len(tmp) == 3:
                    tmp[2] = tmp[2].replace("\n", "")

                if tmp[0].isdigit() and tmp[1].isdigit() and is_country_code(tmp[2]):
                    song_id = tmp[0]
                    user_id = tmp[1]
                    country = tmp[2]

                    # We update the dictionaries of countries and users
                    dict_country[country][song_id] += 1
                    dict_users[user_id][song_id] += 1

                # Monitor memory usage after processing a certain number of lines
                if i % 100000 == 0:
                    memory_usage = psutil.Process().memory_info().rss / (
                        1024**3
                    )  # Memory in GB
                    print(f"Processed {i} lines. Memory Usage: {memory_usage:.2f} GB")

    return dict_country, dict_users
