import os
import json
import re
from config import ALLERGY_FILE, ALLOWED_ALLERGY_NAMES

def load_allergy_data():
    if os.path.exists(ALLERGY_FILE):
        with open(ALLERGY_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_allergy_data(data):
    with open(ALLERGY_FILE, 'w') as f:
        json.dump(data, f)

def apply_allergy_highlight(lines, allergy_numbers):
    highlighted = []
    for line in lines:
        # 괄호 안에서 알러지 번호 추출 (ex. 1.2.3.9 → ["1", "2", "3", "9"])
        found = re.findall(r'\((.*?)\)', line)
        found_nums = set()
        for group in found:
            found_nums.update(group.split("."))

        # 사용자 등록 알러지와 교집합 여부로 취소선 처리
        if set(allergy_numbers) & found_nums:
            highlighted.append(f"~~{line}~~")
        else:
            highlighted.append(line)
    return highlighted