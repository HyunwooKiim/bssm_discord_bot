from discord.ext import commands
from utils.meal_fetcher import fetch_meal
from utils.date_utils import parse_date
from config import MEAL_TYPE, ATPT_OFCDC_SC_CODE, SD_SCHUL_CODE
import aiohttp
import datetime
import os
import discord

MEAL_NAME_NORMALIZE = {
    "조식": "아침",
    "중식": "점심",
    "석식": "저녁"
}

def normalize_meal_name(name):
    return MEAL_NAME_NORMALIZE.get(name, name)

def setup_search_commands(bot):

    @bot.command(name="메뉴검색")
    async def search_menu(ctx, keyword: str, days: int = None):
        today = datetime.datetime.now()
        results = set()
        closest = None

        search_range = days if days else 30

        for delta in range(search_range):
            target_date = today + datetime.timedelta(days=delta)
            date_str = target_date.strftime("%Y%m%d")
            display_date = target_date.strftime("%-m.%d")

            for meal_name, meal_code in MEAL_TYPE.items():
                url = (
                    f"https://open.neis.go.kr/hub/mealServiceDietInfo?"
                    f"KEY={os.getenv('NEIS_API_KEY')}&Type=json&pIndex=1&pSize=1"
                    f"&ATPT_OFCDC_SC_CODE={ATPT_OFCDC_SC_CODE}&SD_SCHUL_CODE={SD_SCHUL_CODE}"
                    f"&MLSV_YMD={date_str}&MMEAL_SC_CODE={meal_code}"
                )
                async with aiohttp.ClientSession() as session:
                    async with session.get(url) as response:
                        data = await response.json()
                try:
                    meal_raw = data['mealServiceDietInfo'][1]['row'][0]['DDISH_NM']
                    if keyword in meal_raw:
                        normalized = normalize_meal_name(meal_name)
                        found = f"{display_date} {normalized}"
                        results.add(found)
                        if not days and not closest:
                            closest = found
                except:
                    continue

        if days:
            if results:
                sorted_results = sorted(results)
                await ctx.send(f"🔍 {days}일 중 '{keyword}'가 포함된 급식:\n" + ", ".join(sorted_results))
            else:
                await ctx.send(f"❌ {days}일 안에 '{keyword}'가 포함된 급식이 없습니다.")
        else:
            if closest:
                await ctx.send(f"🔍 가장 가까운 '{keyword}' 포함 급식: {closest}")
            else:
                await ctx.send(f"❌ 앞으로 30일 안에 '{keyword}'가 포함된 급식이 없습니다.")
