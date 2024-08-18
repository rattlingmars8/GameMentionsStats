import datetime
import asyncpraw
from collections import defaultdict
from fastapi import HTTPException
from src.models.game_mentions import GameMention
from src.config import settings

reddit = asyncpraw.Reddit(
    client_id=settings.reddit.client_id,
    client_secret=settings.reddit.client_secret,
    user_agent=settings.reddit.user_agent,
)
reddit.read_only = True


async def get_reddit_mentions(
    game_name: str,
    start_date: datetime.datetime,
    end_date: datetime.datetime,
) -> dict:
    try:
        if start_date.tzinfo is None:
            start_date = start_date.replace(tzinfo=datetime.timezone.utc)
        if end_date.tzinfo is None:
            end_date = end_date.replace(tzinfo=datetime.timezone.utc)

        mentions_by_date = defaultdict(list)

        matching_subreddits = [
            "Games",
            "gaming",
            "gamernews",
            "GamingLeaksAndRumours",
            "all",
        ]

        for subreddit_name in matching_subreddits:
            subreddit = await reddit.subreddit(subreddit_name)
            async for submission in subreddit.search(game_name):
                submission_date = datetime.datetime.fromtimestamp(
                    submission.created_utc, datetime.timezone.utc
                )

                if start_date <= submission_date <= end_date:
                    mention = GameMention(
                        source=f"Reddit - {subreddit_name}",
                        date=submission_date,
                        description=submission.title,
                        url=submission.shortlink,
                    )
                    mentions_by_date[submission_date.date()].append(mention)

        mentions_summary = []
        for date, mentions in mentions_by_date.items():
            mentions_summary.append(
                {"date": date, "count": len(mentions), "mentions": mentions}
            )

        # Сортування за датою в порядку зростання
        mentions_summary = sorted(mentions_summary, key=lambda x: x["date"])

        return {
            "mentions_summary": mentions_summary,
            "total_results": sum(
                len(mentions) for mentions in mentions_by_date.values()
            ),
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
