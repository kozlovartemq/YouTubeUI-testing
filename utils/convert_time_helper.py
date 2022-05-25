
def convert_str_time_to_secs(time: str) -> int:
    if len(time) > 5:
        mod_time = time.replace(',', '')
        h, m, s = map(int, mod_time.split(':'))
        return h * 3600 + m * 60 + s
    else:
        m, s = map(int, time.split(':'))
        return m * 60 + s


def convert_secs_to_time_str(secs: int) -> str:
    hours = secs // 3600
    minutes = (secs - (hours * 3600)) // 60
    rest_secs = secs - (hours * 3600) - (minutes * 60)
    return f"{str(hours ) +':' if hours != 0 else ''}{minutes}:{rest_secs if rest_secs >= 10 else '0' + str(rest_secs)}"