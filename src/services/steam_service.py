from bs4 import BeautifulSoup

from src.config import settings
from src.utils import make_request
from src.utils.graf_folowers_response_converter import convert_to_custom_json


async def search_game(game_name: str):
    search_url = f"{settings.steam.search_url}{game_name}{settings.steam.search_params}"
    res = await make_request(search_url)

    if not res or "solution" not in res:
        raise Exception("Failed to fetch search results")

    page_content = res["solution"]["response"]
    soup = BeautifulSoup(page_content, "html.parser")

    game_result = soup.find("a", class_="app s-hit-list", href=True)
    if game_result:
        game_id = game_result["data-appid"]
        game_title_tag = game_result.find("span", class_="ais-Highlight")
        game_title = game_title_tag.get_text().strip()
        return game_id, game_title

    raise Exception("Game not found")


async def get_follower_data(game_id: str):
    print("Get Follower")
    followers_api_url = f"{settings.steam.followers_api_call}{game_id}"
    followers_anchor_url = f"https://steamdb.info/app/{game_id}/charts/#followers"
    page = await make_request(followers_anchor_url)
    print(page["solution"]["response"])
    res = await make_request(followers_api_url)
    if not res or "solution" not in res:
        raise Exception("Failed to fetch follower data")
    dirty_data: str = res["solution"]["response"]
    print(convert_to_custom_json(dirty_data.split(';">')[1].split("</")[0]))
    return convert_to_custom_json(dirty_data.split(';">')[1].split("</")[0])
