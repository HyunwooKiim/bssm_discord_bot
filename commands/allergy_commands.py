from discord.ext import commands
from config import ALLOWED_ALLERGY_NAMES
from utils.allergy import load_allergy_data, save_allergy_data

allergy_dict = load_allergy_data()

def setup_allergy_commands(bot):

    @bot.command(name="알러지등록")
    async def register_allergy(ctx, *items):
        user_id = str(ctx.author.id)
        final_allergies = []

        for item in items:
            if item in ALLOWED_ALLERGY_NAMES:
                final_allergies.append(ALLOWED_ALLERGY_NAMES[item])
            elif item.isdigit() and item in ALLOWED_ALLERGY_NAMES.values():
                final_allergies.append(item)

        if not final_allergies:
            await ctx.send("❌ 등록 가능한 알러지 항목이 없습니다.")
            return

        # 기존 알러지에 추가
        existing = set(allergy_dict.get(user_id, []))
        updated = existing.union(final_allergies)

        allergy_dict[user_id] = list(updated)
        save_allergy_data(allergy_dict)
        await ctx.send(f"✅ 알러지 등록 완료: {', '.join(allergy_dict[user_id])}")

    @bot.command(name="내알러지")
    async def my_allergy(ctx):
        user_id = str(ctx.author.id)
        if user_id in allergy_dict:
            nums = allergy_dict[user_id]
            reverse_map = {v: k for k, v in ALLOWED_ALLERGY_NAMES.items()}
            named = [f"{reverse_map.get(num, '?')}({num})" for num in nums]
            await ctx.send(f"📌 등록된 알러지: {', '.join(named)}")
        else:
            await ctx.send("📭 등록된 알러지 정보가 없어요.")

    @bot.command(name="알러지삭제")
    async def delete_allergy(ctx):
        user_id = str(ctx.author.id)
        if user_id in allergy_dict:
            del allergy_dict[user_id]
            save_allergy_data(allergy_dict)
            await ctx.send("✅ 알러지 정보가 삭제되었어요.")
        else:
            await ctx.send("📭 등록된 알러지 정보가 없어요.")