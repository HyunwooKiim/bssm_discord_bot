from discord.ext import commands
from utils.meal_fetcher import fetch_meal
from config import MEAL_TYPE, ATPT_OFCDC_SC_CODE, SD_SCHUL_CODE
import aiohttp
import datetime
import os



def setup_meal_commands(bot):
    @bot.command(name="급식")
    async def meal(ctx, meal_name: str = None, date_str: str = None):
        if meal_name not in MEAL_TYPE:
            await ctx.send(">>> # 📚 급식봇 사용법 안내\n## 🍱 오늘/특정일 급식\n- !급식 아침\n- !급식 점심 내일\n- !급식 저녁 3.21\n## 🔍 메뉴 검색\n- !메뉴검색 치킨\n- !메뉴검색 복숭아 7")
            return

        msg = await fetch_meal(meal_name, ctx.author.id, date_str)
        await ctx.send(msg)

    @bot.command(name="메뉴검색")
    async def search_menu(ctx, keyword: str, days: int = None):
        today = datetime.datetime.now()

        MEAL_NAME_NORMALIZE = {
            "조식": "아침",
            "중식": "점심",
            "석식": "저녁"
        }

        def normalize(meal_name):
            return MEAL_NAME_NORMALIZE.get(meal_name, meal_name)

        if days is None:
            for offset in range(0, 30):
                date = today + datetime.timedelta(days=offset)
                date_str = date.strftime("%Y%m%d")
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
                        meal_data_raw = data['mealServiceDietInfo'][1]['row'][0]['DDISH_NM']
                        if keyword in meal_data_raw:
                            meal_text = '\n'.join(meal_data_raw.split('<br/>'))
                            await ctx.send(
                                f"🔍 '{keyword}'가 포함된 급식 발견!\n\n📅 {date.strftime('%Y-%m-%d')} {normalize(meal_name)}\n{meal_text}"
                            )
                            return
                    except KeyError:
                        continue
            await ctx.send(f"😢 30일 이내 '{keyword}'가 포함된 급식을 찾을 수 없어요.")
        else:
            results = set()
            for offset in range(0, days):
                date = today + datetime.timedelta(days=offset)
                date_str = date.strftime("%Y%m%d")
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
                        meal_data_raw = data['mealServiceDietInfo'][1]['row'][0]['DDISH_NM']
                        if keyword in meal_data_raw:
                            results.append(f"{date.month}.{date.day} {normalize(meal_name)}")
                    except KeyError:
                        continue
            if results:
                await ctx.send(f"🔍 {days}일 중 '{keyword}'가 포함된 급식:\n\n" + ', '.join(sorted(results)))
            else:
                await ctx.send(f"😢 {days}일 중 '{keyword}'가 포함된 급식을 찾을 수 없어요.")
                
