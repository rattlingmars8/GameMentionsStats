# from googleapiclient.discovery import build
# from googleapiclient.errors import HttpError
# from datetime import datetime, timezone
# from fastapi import HTTPException
# from collections import defaultdict
# from src.models.game_mentions import GameMention
# from src.config import settings
#
#
# async def get_youtube_mentions(
#     game_name: str, start_date: datetime, end_date: datetime, page_token: str = None
# ) -> dict:
#     try:
#         youtube = build("youtube", "v3", developerKey=settings.youtube.api_key)
#
#         # Переведення дат у формат RFC 3339 для запиту до API
#         start_date_rfc3339 = start_date.isoformat("T") + "Z"
#         end_date_rfc3339 = end_date.isoformat("T") + "Z"
#
#         # Пошук відео на YouTube
#         response = (
#             youtube.search()
#             .list(
#                 q=game_name,
#                 part="snippet",
#                 type="video",
#                 publishedAfter=start_date_rfc3339,
#                 publishedBefore=end_date_rfc3339,
#                 maxResults=50,
#                 pageToken=page_token,
#             )
#             .execute()
#         )
#
#         mentions_by_date = defaultdict(list)
#
#         for item in response.get("items", []):
#             published_at = datetime.strptime(
#                 item["snippet"]["publishedAt"], "%Y-%m-%dT%H:%M:%SZ"
#             ).replace(tzinfo=timezone.utc)
#             mention = GameMention(
#                 source="YouTube",
#                 date=published_at,
#                 description=item["snippet"]["title"],
#                 url=f"https://www.youtube.com/watch?v={item['id']['videoId']}",
#             )
#             # Групування згадок за датою
#             mentions_by_date[published_at.date()].append(mention)
#
#         mentions_summary = []
#         for date, mentions in mentions_by_date.items():
#             mentions_summary.append(
#                 {"date": date, "count": len(mentions), "mentions": mentions}
#             )
#
#         # Сортування за датою в порядку зростання
#         mentions_summary = sorted(mentions_summary, key=lambda x: x["date"])
#
#         return {
#             "mentions_summary": mentions_summary,
#             "next_page_token": response.get("nextPageToken"),
#             "total_results": response.get("pageInfo", {}).get("totalResults", 0),
#         }
#
#     except HttpError as e:
#         raise HTTPException(
#             status_code=e.resp.status, detail=f"YouTube API Error: {e.content}"
#         )
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
