# Music Streaming Log Processing

This repository hosts a Python script suite designed to process and analyze log data from a music streaming platform. The logs are structured in daily files and each log entry represents a song played by a user and contains information about the song's ID, the user's ID, and their country code.

## Installation

1. Clone the repository.

```bash
git clone https://github.com/your-github-username/music-streaming-log-processing
```

2. Navigate to the project directory

```bash
cd music-streaming-log-processing
```

3. Install the required Python packages.

```bash
pip install -r requirements.txt
```

## Usage

The main scripts of this project are watch_dogs.py, process_7days_log.py, process_daily_log.py, and a set of utility functions.

- The watch_dogs.py script observes the log files directory and runs process_7days_log.py whenever a new log file is added. The log files must follow the format listen-YYYYMMDD.log. It first processes the log files that are already in the directory and then continues to process any new files as they are added.

- The process_7days_log.py script processes the logs from the last 7 days. If a log has already been processed, it will not process it again, which makes the system more efficient. For every unprocessed log, it calculates the top songs by country and by user and stores these results in temporary storage for further processing (tmp_storage directory).

- The process_daily_log.py script processes individual log files. It reads log files in batches to optimize memory management and aggregates the number of times each song was played by each user and in each country. The results are stored in dictionaries and saved to disk.

## Algorithm Explanation

The process_7days_logs function retrieves the last seven log files from the logs directory. If any of these files have already been processed (meaning the top songs by country and by user have been calculated), the function will not process them again. However, if a file has not been seen before, the function calls the process_daily_log function, which processes the log file in batches to improve memory management. As it processes the log file, it performs a check on the value of the log and drops any eventual corrupted values. After that, it aggregates the number of times each song was played, both by country and by user. For each log file (representing a day), the function saves the results to disk as a JSON file. This saved data is then used to avoid processing the same file repeatedly when calculating the top songs over the last seven days. Essentially, the function calculates the top songs for each day and then sums these top songs over a seven-day period. The get_top_song/user function reads the JSON files corresponding to the last seven days, performs an aggregate, and retrieves the top 50 songs. The final results are saved in the 'country_top50_YYYYMMDD' and 'user_top50_YYYYMMDD' files.

## How to run it every day to compute the files.

To run the scripts every day and compute the files, you can set up a watch file using the watchdog library. This system will observe the log directory, and when a new file is added, it will automatically process the script to get the top songs by country and user. To further automate the process, you can set up the watch_dogs script as a background daemon that runs autonomously. It can periodically check if a new file has been added and compute the results accordingly.

## To go further

- Verify if the last log files correspond to the last 7 days accurately not only the last 7 log files.
- Make the scripts more modular to compute not only the top songs for the last 7 days but also, for example, the top 10 songs in the last year.
- Implement parallelism (MapReduce) to process the log files more efficiently, considering there are more than 30 million listens per day.
- Improve the log information of the demon.
