from datetime import timedelta


def timedelta_to_str(td: timedelta) -> str:
    """Преобразует строку ISO 8601 в дни, часы, минуты и секунды."""
    total_seconds = int(td.total_seconds())
    days = total_seconds // 86400
    hours = (total_seconds % 86400) // 3600
    minutes = (total_seconds % 3600) // 60
    seconds = total_seconds % 60
    microseconds = td.microseconds
    return (f'{days} days {hours} hours {minutes} minutes '
            f'{seconds} seconds {microseconds} microseconds')
