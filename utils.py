import os
import json


# Get the list of log files in the logs folder
def get_log_name():
    arr = os.listdir("logs")
    return arr


# Get the date of a given log file
def get_log_date(log_name):
    return log_name.split("-")[1].split(".")[0]


def get_last_7_days(path):
    logs_to_process = os.listdir(path)
    logs_to_process.sort(reverse=True)
    last_7_logs = logs_to_process[:7]
    return last_7_logs


# Check if a string is a country code
def is_country_code(string):
    if len(string) == 2:
        for char in string:
            if not char.isalpha():
                return False
        return True
    return False


# We save intermediate results to disk
def save_dict_to_file(dictionary, dir, date):
    os.makedirs(dir, exist_ok=True)
    with open(dir + "/" + date, "w") as file:
        json.dump(dictionary, file)


# We load intermediate results from disk
def load_dict_from_file(file_path):
    with open(file_path, "r") as file:
        dictionary = json.load(file)
    return dictionary
