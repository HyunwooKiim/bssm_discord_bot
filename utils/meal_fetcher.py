import aiohttp
from config import ATPT_OFCDC_SC_CODE, SD_SCHUL_CODE, MEAL_TYPE
from utils.date_parser import parse_date
from utils.allergy import apply_allergy_highlight
import datetime
import os
from dotenv import load_dotenv
load_dotenv()
NEIS_API_KEY = os.getenv("NEIS_API_KEY")

async def fetch_meal(meal_name, user_id=None, date_str=None, allergy_dict=None):
    if date_str is None:
        date = datetime.datetime.now()
    else:
        date = parse_date(date_str)
        if date is None:
            return "❌ 날짜 형식이 올바르지 않아요. 예: 3/20, 3.20, 3월20일, 내일"

    formatted_date = date.strftime("%Y%m%d")
    meal_code = MEAL_TYPE.get(meal_name)

    url = (
        f"https://open.neis.go.kr/hub/mealServiceDietInfo?"
        f"KEY={NEIS_API_KEY}&Type=json&pIndex=1&pSize=1"
        f"&ATPT_OFCDC_SC_CODE={ATPT_OFCDC_SC_CODE}&SD_SCHUL_CODE={SD_SCHUL_CODE}"
        f"&MLSV_YMD={formatted_date}&MMEAL_SC_CODE={meal_code}"
    )

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            data = await response.json()

    try:
        meal_data_raw = data['mealServiceDietInfo'][1]['row'][0]['DDISH_NM']
        meal_lines = meal_data_raw.split('<br/>')
        allergy_numbers = allergy_dict.get(str(user_id), []) if allergy_dict else []
        highlighted_lines = apply_allergy_highlight(meal_lines, allergy_numbers)
        meal_data = '\n'.join(highlighted_lines)
        return f">>> ## 📅 {date.strftime('%Y-%m-%d')} {meal_name} 급식:\n{meal_data}"
    except KeyError:
        return f"😢 {date.strftime('%Y-%m-%d')} {meal_name} 급식 정보를 불러올 수 없어요."
