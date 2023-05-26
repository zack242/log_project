import psutil
import logging
from collections import defaultdict
from utils import is_country_code
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

BATCH_SIZE = int(os.environ.get("BATCH_SIZE"))

# Configure logging settings
logging.basicConfig(
    filename="log/daemon.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)


def process_daily_log(log_files):
    # We initialize two dictionaries, one for countries and one for users
    dict_country = defaultdict(lambda: defaultdict(int))
    dict_users = defaultdict(lambda: defaultdict(int))

    # We iterate through the log file
    with open("logs/" + log_files, "r") as f:
        lines = f.readlines()
        batch_size = BATCH_SIZE
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
                if i % BATCH_SIZE == 0:
                    memory_usage = psutil.Process().memory_info().rss / (
                        1024**3
                    )  # Memory in GB
                    logging.info(
                        f"Processed {i} lines. Memory Usage: {memory_usage:.2f} GB"
                    )

    return dict_country, dict_users
