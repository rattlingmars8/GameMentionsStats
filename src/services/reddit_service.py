import aiohttp
import asyncio
import logging
import datetime
from collections import defaultdict
from typing import Optional, Dict, Any
from fastapi import HTTPException

from src.models.game_mentions import GameMention

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

BASE_URL = "https://api.pullpush.io/reddit/search/submission/"


async def fetch_reddit_submissions(
    session: aiohttp.ClientSession,
    *,
    q: Optional[str] = None,
    title: Optional[str] = None,
    selftext: Optional[str] = None,
    size: int = 100,
    sort: str = None,
    sort_type: str = None,
    author: Optional[str] = None,
    subreddit: Optional[str] = None,
    after: Optional[int] = None,
    before: Optional[int] = None,
    score: Optional[str] = None,
    num_comments: Optional[str] = None,
    over_18: Optional[str] = None,
    is_video: Optional[str] = None,
    locked: Optional[str] = None,
    stickied: Optional[str] = None,
    spoiler: Optional[str] = None,
    contest_mode: Optional[str] = None,
) -> Dict[str, Any]:

    params = {
        "q": q,
        "title": title,
        "selftext": selftext,
        "size": size,
        "sort": sort,
        "sort_type": sort_type,
        "author": author,
        "subreddit": subreddit,
        "after": after,
        "before": before,
        "score": score,
        "num_comments": num_comments,
        "over_18": over_18,
        "is_video": is_video,
        "locked": locked,
        "stickied": stickied,
        "spoiler": spoiler,
        "contest_mode": contest_mode,
    }

    filtered_params = {key: value for key, value in params.items() if value is not None}

    try:
        logger.info(f"Fetching data from {BASE_URL} with params: {filtered_params}")
        async with session.get(BASE_URL, params=filtered_params) as response:
            response.raise_for_status()
            json_data = await response.json()
            logger.info(f"Received {len(json_data.get('data', {}))} results")
            return json_data

    except aiohttp.ClientError as e:
        logger.error(f"HTTP request failed: {str(e)}")
        raise
    except asyncio.TimeoutError:
        logger.error("The request timed out.")
        raise
    except Exception as e:
        logger.error(f"An unexpected error occurred: {str(e)}")
        raise


async def get_reddit_mentions(
    game_name: str,
    start_date: datetime.datetime,
    end_date: datetime.datetime,
) -> Dict[str, Any]:
    try:
        if start_date.tzinfo is None:
            start_date = start_date.replace(tzinfo=datetime.timezone.utc)
        if end_date.tzinfo is None:
            end_date = end_date.replace(tzinfo=datetime.timezone.utc)

        epoch_start = int(start_date.timestamp())
        epoch_end = int(end_date.timestamp())

        mentions_by_date = defaultdict(list)

        async with aiohttp.ClientSession() as session:
            after = epoch_start
            before = epoch_end

            while True:
                data = await fetch_reddit_submissions(
                    session,
                    q=game_name,
                    after=after,
                    before=before,
                    selftext=game_name,
                    title=game_name,
                )

                posts = data.get("data", {})
                print("post len - ", len(posts))
                if not posts:
                    logger.info("No more posts retrieved.")
                    break

                logger.info(f"Retrieved {len(posts)} posts from Reddit API")

                for post in posts:
                    created_utc = post.get("created_utc")
                    submission_date = datetime.datetime.fromtimestamp(
                        created_utc, datetime.timezone.utc
                    )

                    if submission_date < start_date:
                        logger.info(
                            f"Post from {submission_date} is outside the date range."
                        )
                        continue

                    # if (
                    #     game_name.lower() in post.get("selftext", "").lower()
                    #     or game_name.lower() in post.get("title", "").lower()
                    # ):
                    mention = GameMention(
                        source=f"Reddit API - r/{post.get('subreddit')}",
                        date=submission_date,
                        description=post.get("title"),
                        url=f"https://www.reddit.com{post.get('permalink')}",
                    )
                    mentions_by_date[submission_date.date()].append(mention)
                    logger.info(f"Found mention: {mention}")

                # Оновлюємо before для пагінації
                before = int(posts[-1]["created_utc"])
                print("After", after)
                if not before or before > epoch_end:
                    logger.info("No more pages or reached the end date.")
                    break

                await asyncio.sleep(1)

        mentions_summary = [
            {"date": date, "count": len(mentions), "mentions": mentions}
            for date, mentions in mentions_by_date.items()
        ]

        mentions_summary = sorted(mentions_summary, key=lambda x: x["date"])
        total_results = sum(len(mentions) for mentions in mentions_by_date.values())
        logger.info(f"Total results found: {total_results}")

        return {
            "mentions_summary": mentions_summary,
            "total_results": total_results,
        }

    except Exception as e:
        logger.exception("An error occurred during the search")
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
