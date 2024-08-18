from fastapi import APIRouter, Query, HTTPException

from src.models.error_model import ErrorResponse
from src.services.reddit_service import get_reddit_mentions
from src.models.game_mentions import Response, DateRangeEnum
from src.services.steam_service import search_game, get_follower_data

from src.utils import calculate_date_range

router = APIRouter(tags=["Game Data"])


@router.get(
    "/{game_name}",
    response_model=Response,
    responses={
        400: {"description": "Bad Request", "model": ErrorResponse},
        500: {"description": "Internal Server Error", "model": ErrorResponse},
    },
)
async def get_game_data(
    game_name: str,
    date_range: DateRangeEnum = Query(
        ...,
        description="Choose a date range: week, month, three_months, six_months, year",
    ),
):
    if len(game_name) < 2:
        raise HTTPException(
            status_code=400, detail="Game name must be at least 2 characters long."
        )

    start_date, end_date = calculate_date_range(date_range)

    try:
        reddit_data = await get_reddit_mentions(game_name, start_date, end_date)
        mentions_summary = reddit_data["mentions_summary"]
        total_results = reddit_data["total_results"]

        game_id, game_title = await search_game(game_name)
        print(f"Found Game: {game_title} with ID: {game_id}")
        stats = await get_follower_data(game_id)

        return Response(
            results=mentions_summary, total_results=total_results, stats=stats
        )

    except HTTPException as e:
        raise e
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Internal Server Error")
