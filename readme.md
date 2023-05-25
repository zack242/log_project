Copy code

# Music Streaming Log Processing

This repository hosts a Python script suite designed to process and analyze log data from a music streaming platform. The logs are structured in daily files and each log entry represents a song played by a user and contains information about the song's ID, the user's ID, and their country code.

## Installation

1. Clone the repository.

```bash
git clone https://github.com/your-github-username/music-streaming-log-processing
Navigate to the project directory.
bash
Copy code
cd music-streaming-log-processing
Install the required Python packages.
bash
Copy code
pip install -r requirements.txt
Usage

The main scripts of this project are watch_dogs.py, process_7days_log.py, process_daily_log.py and a set of utility functions.

The watch_dogs.py script observes the log files directory and runs process_7days_log.py whenever a new log file is added. It first processes the log files that are already in the directory, and then continues to process any new files as they are added.

The process_7days_log.py script processes the logs from the last 7 days. If a log has already been processed, it will not process it again, which makes the system more efficient. For every unprocessed log, it calculates the top songs by country and by user, and stores these results in temporary storage for further processing.

The process_daily_log.py script processes individual log files. It reads log files in batches to optimize memory management, and it aggregates the number of times each song was played by each user and in each country. The results are stored in dictionaries and saved to disk.

Algorithm Explanation

The process_7days_logs function retrieves the last seven log files from the logs directory. If any of these files have already been processed (meaning, the top songs by country and by user have been calculated), the function will not process it again. However, if a file has not been seen before, the function calls the process_daily_log function, which processes the log file in batches to improve memory management. As it processes the log file, it performs an aggregate of the number of times each song was played, both by country and by user. For each log file (representing a day), the function saves the results in disk as a JSON file. This saved data is then used to avoid processing the same file repeatedly when calculating the top songs over the last seven days. Essentially, the function calculates the top songs for each day and then sums these top songs over a seven-day period. The get_top_song/user function reads the JSON files corresponding to the last seven days, performs an aggregate, and retrieves the top 50 songs. The final results are saved in the 'top_song_country' and 'top_song_user' files.

```
