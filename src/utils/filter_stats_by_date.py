from datetime import datetime


def filter_stats_by_date(stats, start_date, end_date):

    start_date = start_date.date()
    end_date = end_date.date()

    filtered_stats = []

    for stat in stats:
        stat_date = datetime.strptime(stat["date"], "%Y-%m-%d").date()
        if start_date <= stat_date <= end_date:
            filtered_stats.append(stat)

    return filtered_stats
