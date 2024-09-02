from datetime import datetime, timedelta
from fastapi import HTTPException

from src.models.game_mentions import DateRangeEnum

DATE_RANGES = {
    DateRangeEnum.week: timedelta(weeks=1),
    DateRangeEnum.month: timedelta(days=30),
    DateRangeEnum.three_months: timedelta(days=90),
    DateRangeEnum.six_months: timedelta(days=180),
    DateRangeEnum.year: timedelta(days=365),
}


def calculate_date_range(date_range: DateRangeEnum) -> tuple:
    end_date = datetime.now()

    delta = DATE_RANGES.get(date_range.value)

    if not delta:
        raise HTTPException(status_code=400, detail="Invalid date range")

    start_date = end_date - delta
    print(start_date, end_date)

    return start_date, end_date
