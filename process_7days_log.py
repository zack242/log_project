from utils import get_last_7_days, get_log_date, save_dict_to_file
from process_daily_log import process_daily_log


def process_7days_logs(path):
    logs = get_last_7_days(path)

    for log in logs:
        date = get_log_date(log)
        country, users = process_daily_log(log)
        save_dict_to_file(country, "country_data", date)
        save_dict_to_file(users, "user_data", date)
