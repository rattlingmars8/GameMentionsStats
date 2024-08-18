import json
from datetime import datetime, timedelta


def convert_to_custom_json(json_string: str):
    data = json.loads(json_string)

    if data.get("success") and "data" in data:
        start_epoch = data["data"]["start"]
        step_seconds = data["data"]["step"]
        values = data["data"]["values"]

        custom_data = []

        start_date = datetime.fromtimestamp(start_epoch)

        for i, followers in enumerate(values):
            date = start_date + timedelta(seconds=i * step_seconds)
            custom_data.append(
                {
                    "date": date.strftime(
                        "%Y-%m-%d"
                    ),  # Зберігаємо дату у форматі 'YYYY-MM-DD'
                    "followers": followers,
                }
            )

        return custom_data

    else:
        raise ValueError("Invalid JSON format")
