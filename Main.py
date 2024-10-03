import interactions,os,random,shutil,asyncio,time
from config import DICE_CATEGORIES,TECHNIQUES_CHANCES,PERMISSIONS,RANKS,TECHNIQUE_LIBRARIES,BOT_NAME,GUILD_NAME,GUILD_ID,BOT_TOKEN,OWNER_NAME
from interactions import SlashContext,slash_command,slash_option,OptionType,listen,Client,SlashCommandChoice,Member,Embed,Message,Intents
from interactions.api.events import MessageCreate
from datetime import datetime, timedelta

bot=Client(token=BOT_TOKEN,intents=Intents.DEFAULT | Intents.MESSAGE_CONTENT)

@listen()
async def on_ready():
    print(BOT_NAME,"запущен и успешно работает.")
    print("Мой токен -",BOT_TOKEN)
    print("ID сервера -",GUILD_ID)
    print(GUILD_NAME,"and",OWNER_NAME,"ONE LOVES! ♡")

@listen()
async def check_permissions(ctx:SlashContext,command_name:str):
    user_roles=[role.name for role in ctx.author.roles]
    allowed_roles=PERMISSIONS.get(command_name,[])
    if not any(role in allowed_roles for role in user_roles):
        await ctx.send("У вас нет прав для использования этой команды.",ephemeral=True)
        return False
    return True

@listen()
async def on_message_create(event:MessageCreate):
    if event.message.content.startswith(("//", "/)", ")/", "/", "(", "/(", "(/")):
        await event.message.delete(delay=60)
    if event.message.content.startswith(("(")) and event.message.content.endswith((")")):
        await event.message.delete(delay=60)

@slash_command(name="создать_персонажа",description="Создает нового персонажа", dm_permission=False)
@slash_option(
    name="member",
    description="Пользователь, для которого вы хотите создать персонажа",
    required=True,
    opt_type=OptionType.USER
)
@slash_option(
    name="имя",
    description="Имя персонажа",
    required=True,
    opt_type=OptionType.STRING
)
@slash_option(
    name="фамилия",
    description="Фамилия персонажа",
    required=True,
    opt_type=OptionType.STRING
)
@slash_option(
    name="возраст",
    description="Возраст персонажа",
    required=True,
    opt_type=OptionType.INTEGER
)
@slash_option(
    name="раса",
    description="Раса персонажа",
    required=True,
    opt_type=OptionType.STRING,
    choices=[
        SlashCommandChoice(name="Человек", value="Человек"),
        SlashCommandChoice(name="Проклятье", value="Проклятье"),   
        SlashCommandChoice(name="Картина смерти", value="Картина смерти")
    ]
)
@slash_option(
    name="клан",
    description="Клан персонажа",
    required=True,
    opt_type=OptionType.STRING,
    choices=[
        SlashCommandChoice(name="Отсутствует", value="Отсутствует"),
        SlashCommandChoice(name="Камо", value="Камо"),
        SlashCommandChoice(name="Дзенин", value="Дзенин"),   
        SlashCommandChoice(name="Инумаки", value="Инумаки"),
        SlashCommandChoice(name="Гето", value="Гето"),
        SlashCommandChoice(name="Фудзивара", value="Фудзивара"),
        SlashCommandChoice(name="Годжо", value="Годжо"),
        SlashCommandChoice(name="Рёмен", value="Рёмен")
    ]
)
@slash_option(
    name="титул",
    description="Титул персонажа",
    required=True,
    opt_type=OptionType.STRING,
    choices=[
        SlashCommandChoice(name="Отсутствует", value="Отсутствует"),
        SlashCommandChoice(name="Мастер боя", value="Мастер боя"),   
        SlashCommandChoice(name="Чудовище", value="Чудовище"),
        SlashCommandChoice(name="Бывший ученик Киото", value="Бывший ученик Киото"),
        SlashCommandChoice(name="Мастер барьеров", value="Мастер барьеров"),
        SlashCommandChoice(name="Проклятый", value="Проклятый"),
        SlashCommandChoice(name="Зайчик", value="Зайчик"),
        SlashCommandChoice(name="Жалкая обезьяна", value="Жалкая обезьяна"),
        SlashCommandChoice(name="Неубиваемый", value="Неубиваемый"),
        SlashCommandChoice(name="Одарённый", value="Одарённый"),
        SlashCommandChoice(name="Король проклятий", value="Король проклятий")
    ]
)
@slash_option(
    name="уровень",
    description="Уровень персонажа",
    required=True,
    opt_type=OptionType.STRING,
    choices=[
        SlashCommandChoice(name="Четвёртый", value="Четвёртый"),
        SlashCommandChoice(name="Третий", value="Третий"),
        SlashCommandChoice(name="Второй", value="Второй"),
        SlashCommandChoice(name="Первый", value="Первый"),
        SlashCommandChoice(name="Особый", value="Особый")
    ]
)
@slash_option(
    name="проклятье",
    description="Проклятье персонажа",
    required=True,
    opt_type=OptionType.STRING,
    choices=[
        SlashCommandChoice(name="Отсутствует", value="Отсутствует"),
        SlashCommandChoice(name="Небесное проклятье", value="Небесное проклятье"),
        SlashCommandChoice(name="Небесное ограничение", value="Небесное ограничение")
    ]
)
@slash_option(
    name="внешность",
    description="Внешность персонажа ( Ссылка )",
    required=True,
    opt_type=OptionType.STRING
)
async def create_character(ctx:SlashContext, member:Member, имя:str, фамилия:str, клан:str, титул:str, проклятье:str, возраст:int, внешность:str, уровень:str, раса:str):
    if not await check_permissions(ctx, "персонаж"):
        return
    user_folder_path = os.path.join("General", member.username)
    character_folder_path = os.path.join(user_folder_path, "Character")
    if os.path.exists(character_folder_path):
        await ctx.send(f"Для пользователя {member.username} уже создан персонаж.", ephemeral=True)
        return
    user_folder_path = os.path.join("General", member.username)
    os.makedirs(user_folder_path, exist_ok=True)
    character_folder_path = os.path.join(user_folder_path, "Character")
    os.makedirs(character_folder_path, exist_ok=True)
    with open(os.path.join(character_folder_path, "внешность.txt"), "w") as f:
        f.write(внешность)
    with open(os.path.join(character_folder_path, "возраст.txt"), "w") as f:
        f.write(str(возраст))
    with open(os.path.join(character_folder_path, "имя.txt"), "w") as f:
        f.write(имя)
    with open(os.path.join(character_folder_path, "клан.txt"), "w") as f:
        f.write(клан)
    with open(os.path.join(character_folder_path, "проклятье.txt"), "w") as f:
        f.write(проклятье)
    with open(os.path.join(character_folder_path, "уровень.txt"), "w") as f:
        f.write(уровень)
    with open(os.path.join(character_folder_path, "титул.txt"), "w") as f:
        f.write(титул)
    with open(os.path.join(character_folder_path, "фамилия.txt"), "w") as f:
        f.write(фамилия)
    with open(os.path.join(character_folder_path, "раса.txt"), "w") as f:
        f.write(раса)
    inventory_folder_path = os.path.join(user_folder_path, "Inventory")
    os.makedirs(inventory_folder_path, exist_ok=True)
    with open(os.path.join(inventory_folder_path, "wallet.txt"), "w") as f:
        f.write("5000")
    os.makedirs(os.path.join(inventory_folder_path, "Items"), exist_ok=True)
    stats_folder_path = os.path.join(user_folder_path, "Stats")
    os.makedirs(stats_folder_path, exist_ok=True)
    stats_subfolders = ["Stats", "Techniques"]
    for subfolder in stats_subfolders:
        os.makedirs(os.path.join(stats_folder_path, subfolder), exist_ok=True)
    stats_files = ["восприятие.txt", "выброс.txt", "выносливость.txt", "запас.txt", "свойство.txt", "сила.txt", "скорость.txt", "стойкость.txt"]
    for stat in stats_files:
        with open(os.path.join(stats_folder_path, "Stats", stat), "w") as f:
            f.write("0\n0")
    techniques_files = ["барьеры.txt", "ОПТ.txt", "РТ.txt", "ЧМ.txt", "ПТ.txt", "Эмоция.txt", "Корзина.txt", "РП.txt"]
    for technique in techniques_files:
        with open(os.path.join(stats_folder_path, "Techniques", technique), "w") as f:
            f.write("0")
    await member.add_role(1285592988927660102)
    await ctx.send(f"Персонаж для {member.username} успешно создан!")

@slash_command(name="карточка", description="Показывает информацию о персонаже")
@slash_option(
    name="member",
    description="Пользователь, карточку персонажа которого вы хотите увидеть",
    required=False,
    opt_type=OptionType.USER
)
async def view_character(ctx: SlashContext, member:Member = None):
    if member is None:
        member = ctx.author
    character_folder_path = os.path.join("General", member.username, "Character")
    if not os.path.exists(character_folder_path):
        await ctx.send(f"У пользователя {member.username} нет созданного персонажа.", ephemeral=True)
        return

    with open(os.path.join(character_folder_path, "уровень.txt"), "r") as f:
        level = f.read()
    with open(os.path.join(character_folder_path, "раса.txt"), "r") as f:
        race = f.read()

    # Определи путь к изображению ранга
    if race == "Человек":
        if level == "Четвёртый":
            rank_path = "https://message.style/cdn/images/36c0f1a84ba9ec42ecb91081a4f3fc18d7d695dc0450f47b9d5262545c9ea6df.png"
        elif level == "Третий":
            rank_path = "https://message.style/cdn/images/721b49fe89bbb2dc16d75ae5a439b78aa28d2a049280ed9cb451d789c2124277.png"
        elif level == "Второй":
            rank_path = "https://message.style/cdn/images/29dd040c8b6db8f6cfa0cff229784cd82757602fab13ced4651b8e8eb5c06e48.png"
        elif level == "Первый":
            rank_path = "https://message.style/cdn/images/570d5f1dc8623257f60aa3c1be0eea17d52029d91f9a31f582e41ae94fea470c.png"
        elif level == "Особый":
            rank_path = "https://message.style/cdn/images/28be9f6ce15559120ab57400c4df4f2062fae57afc782b19b8fe7ee11150d0bf.png"
    elif race == "Проклятье" or "Картина смерти":
        if level == "Четвёртый":
            rank_path = "https://message.style/cdn/images/68bac2ecf410c8e12f752b0b140815442ba4612ea08a97ca31d3d4cc7b0756b7.png"
        elif level == "Третий":
            rank_path = "https://message.style/cdn/images/bf8789b55e4cf3b1e577d23b1e6e0219827b044e0aa68875c2e7082c57e5940c.png"
        elif level == "Второй":
            rank_path = "https://message.style/cdn/images/1214a5c8669810a2012ac449d78f2d878998589ab8eafc005b942f8198b36822.png"
        elif level == "Первый":
            rank_path = "https://message.style/cdn/images/1c0e6c0372b4ed4dd413abae2dc1096ffcc42d387acb162b1fed09605d1f46db.png"
        elif level == "Особый":
            rank_path = "https://message.style/cdn/images/e76bd16dc55e62f01a9168deea9b5881d314c0b67322f40c8d4bed14e77a2386.png"

    # Установить миниатюру с помощью URL-адреса загруженного изображения
    embed = interactions.Embed(
        color=0xFF9933
    )
    embed.set_author(name=f"{member.username}", icon_url=member.avatar_url)
    with open(os.path.join(character_folder_path, "имя.txt"), "r") as f:
        first_name = f.read()
    with open(os.path.join(character_folder_path, "фамилия.txt"), "r") as f:
        last_name = f.read()
    embed.title = f"{first_name} {last_name}"
    with open(os.path.join(character_folder_path, "внешность.txt"), "r") as f:
        embed.set_image(url=f.read())
    with open(os.path.join(character_folder_path, "возраст.txt"), "r") as f:
        embed.add_field(name="Возраст", value=f.read(), inline=True)
    with open(os.path.join(character_folder_path, "раса.txt"), "r") as f:
        embed.add_field(name="Раса", value=f.read(), inline=True)
    with open(os.path.join(character_folder_path, "клан.txt"), "r") as f:
        embed.add_field(name="Клан", value=f.read())
    with open(os.path.join(character_folder_path, "титул.txt"), "r") as f:
        embed.add_field(name="Титул", value=f.read())
    with open(os.path.join(character_folder_path, "проклятье.txt"), "r") as f:
        embed.add_field(name="Проклятье", value=f.read())
    embed.set_thumbnail(url=rank_path)
    await ctx.send(embed=embed)

@slash_command(name="изменить_персонажа", description="Изменяет информацию о персонаже", dm_permission=False)
@slash_option(
    name="member",
    description="Пользователь, персонажа которого вы хотите изменить",
    required=True,
    opt_type=OptionType.USER
)
@slash_option(
    name="имя",
    description="Новое имя персонажа",
    required=False,
    opt_type=OptionType.STRING
)
@slash_option(
    name="фамилия",
    description="Новая фамилия персонажа",
    required=False,
    opt_type=OptionType.STRING
)
@slash_option(
    name="возраст",
    description="Новый возраст персонажа",
    required=False,
    opt_type=OptionType.INTEGER
)
@slash_option(
    name="раса",
    description="Новая раса персонажа",
    required=False,
    opt_type=OptionType.STRING,
    choices=[
        SlashCommandChoice(name="Человек", value="Человек"),
        SlashCommandChoice(name="Проклятье", value="Проклятье"),   
        SlashCommandChoice(name="Картина смерти", value="Картина смерти")
    ]
)
@slash_option(
    name="клан",
    description="Новый клан персонажа",
    required=False,
    opt_type=OptionType.STRING,
    choices=[
        SlashCommandChoice(name="Отсутствует", value="Отсутствует"),
        SlashCommandChoice(name="Камо", value="Камо"),
        SlashCommandChoice(name="Дзенин", value="Дзенин"),   
        SlashCommandChoice(name="Инумаки", value="Инумаки"),
        SlashCommandChoice(name="Гето", value="Гето"),
        SlashCommandChoice(name="Фудзивара", value="Фудзивара"),
        SlashCommandChoice(name="Годжо", value="Годжо"),
        SlashCommandChoice(name="Рёмен", value="Рёмен")
    ]
)
@slash_option(
    name="титул",
    description="Новый титул персонажа",
    required=False,
    opt_type=OptionType.STRING,
    choices=[
        SlashCommandChoice(name="Отсутствует", value="Отсутствует"),
        SlashCommandChoice(name="Мастер боя", value="Мастер боя"),   
        SlashCommandChoice(name="Чудовище", value="Чудовище"),
        SlashCommandChoice(name="Бывший ученик Киото", value="Бывший ученик Киото"),
        SlashCommandChoice(name="Мастер барьеров", value="Мастер барьеров"),
        SlashCommandChoice(name="Проклятый", value="Проклятый"),
        SlashCommandChoice(name="Зайчик", value="Зайчик"),
        SlashCommandChoice(name="Жалкая обезьяна", value="Жалкая обезьяна"),
        SlashCommandChoice(name="Неубиваемый", value="Неубиваемый"),
        SlashCommandChoice(name="Одарённый", value="Одарённый"),
        SlashCommandChoice(name="Король проклятий", value="Король проклятий")
    ]
)
@slash_option(
    name="уровень",
    description="Новый уровень персонажа",
    required=False,
    opt_type=OptionType.STRING,
    choices=[
        SlashCommandChoice(name="Четвёртый", value="Четвёртый"),
        SlashCommandChoice(name="Третий", value="Третий"),
        SlashCommandChoice(name="Второй", value="Второй"),
        SlashCommandChoice(name="Первый", value="Первый"),
        SlashCommandChoice(name="Особый", value="Особый")
    ]
)
@slash_option(
    name="проклятье",
    description="Новое проклятье персонажа",
    required=False,
    opt_type=OptionType.STRING,
    choices=[
        SlashCommandChoice(name="Отсутствует", value="Отсутствует"),
        SlashCommandChoice(name="Небесное проклятье", value="Небесное проклятье"),
        SlashCommandChoice(name="Небесное ограничение", value="Небесное ограничение")
    ]
)
@slash_option(
    name="внешность",
    description="Новая внешность персонажа ( Cсылка )",
    required=False,
    opt_type=OptionType.STRING
)
async def manage_character(ctx: SlashContext, member:Member, **kwargs):
    if not await check_permissions(ctx, "персонаж"):
        return
    if not any(kwargs.values()):
        await ctx.send("Вы должны указать хотя бы одну опцию для изменения.", ephemeral=True)
        return
    character_folder_path = os.path.join("General", member.username, "Character")
    if not os.path.exists(character_folder_path):
        await ctx.send(f"У пользователя {member.username} нет созданного персонажа.", ephemeral=True)
        return
    for field, value in kwargs.items():
        if value is not None:
            with open(os.path.join(character_folder_path, f"{field}.txt"), "w") as f:
                if field == "возраст":
                    f.write(str(value))
                else:
                    f.write(value)
    await ctx.send(f"Информация о персонаже {member.username} успешно изменена!")

@slash_command(name="удалить_персонажа", description="Удаляет персонажа пользователя", dm_permission=False)
@slash_option(
    name="member",
    description="Пользователь, персонажа которого вы хотите удалить",
    required=True,
    opt_type=OptionType.USER
)
async def delete_character(ctx: SlashContext, member:Member):
    if not await check_permissions(ctx, "персонаж"):
        return
    user_folder_path = os.path.join("General", member.username)
    if not os.path.exists(user_folder_path):
        await ctx.send(f"У пользователя {member.username} нет созданного персонажа.", ephemeral=True)
        return
    try:
        shutil.rmtree(user_folder_path)
        await member.remove_role(1285592988927660102)
        await ctx.send(f"Персонаж пользователя {member.username} успешно удалён.")
    except OSError as e:
        await ctx.send(f"Не удалось удалить персонажа пользователя {member.username}: {e}")

@slash_command(name="крутка", description="Случайная генерация параметров персонажа")
async def spin(ctx: SlashContext):
    clan = random_choice(DICE_CATEGORIES["Клан"])
    title = random_choice(DICE_CATEGORIES["Титул"])
    curse = random_choice(DICE_CATEGORIES["Проклятье"])
    if curse == "Небесное ограничение":
        curse_property = "Отсутствует проклятая энергия"
    else:
        curse_property = random_choice(DICE_CATEGORIES["Свойство проклятой энергии"])
    if curse == "Небесное ограничение" and clan != "Отсутствует":
        technique = "Отсутствует проклятая энергия"
    elif clan != "Отсутствует":
        technique = random_choice(TECHNIQUES_CHANCES[clan])
    else:
        technique = None
    result = f"Клан: {clan}\n"
    result += f"Титул: {title}\n"
    result += f"Проклятье: {curse}\n"
    result += f"Свойство проклятой энергии: {curse_property}\n"

    if technique is not None:
        result += f"Врождённая клановая техника: {technique}"
    await ctx.send(result)
def random_choice(probabilities: dict) -> str:
    total_probability = sum(probabilities.values())
    random_value = random.uniform(0, total_probability)
    cumulative_probability = 0
    for key, probability in probabilities.items():
        cumulative_probability += probability
        if random_value <= cumulative_probability:
            return key
    return "Отсутствует"

@slash_command(name="статы", description="Показывает статы персонажа")
@slash_option(
    name="отображение",
    description="Как отобразить статы",
    required=True,
    opt_type=OptionType.STRING,
    choices=[
        SlashCommandChoice(name="Цифры", value="цифры"),
        SlashCommandChoice(name="Буквы", value="буквы")
    ]
)
@slash_option(
    name="member",
    description="Пользователь, статы персонажа которого вы хотите увидеть",
    required=False,
    opt_type=OptionType.USER
)
async def show_stats(ctx: SlashContext, отображение: str, member: interactions.User = None ):
    if member is None:
        member = ctx.author
    character_folder_path = os.path.join("General", member.username, "Character")
    stats_folder_path = os.path.join("General", member.username, "Stats", "Stats")
    if not os.path.exists(character_folder_path) or not os.path.exists(stats_folder_path):
        await ctx.send(f"У пользователя {member.username} нет созданного персонажа.", ephemeral=True)
        return
    with open(os.path.join(character_folder_path, "имя.txt"), "r") as f:
        first_name = f.read()
    with open(os.path.join(character_folder_path, "фамилия.txt"), "r") as f:
        last_name = f.read()
    embed = interactions.Embed(
        color=0xFF9933
    )
    embed.set_author(name=f"{member.username}", icon_url=member.avatar_url)
    embed.title = f"{first_name} {last_name}"
    stats_files = ["сила.txt", "скорость.txt", "стойкость.txt", "выносливость.txt", "запас.txt", "выброс.txt", "восприятие.txt", "свойство.txt"]
    for stat_file in stats_files:
        with open(os.path.join(stats_folder_path, stat_file), "r") as f:
            stats = f.read().strip().split("\n")
            stat_name = stat_file[:-4].capitalize()
            stat_points = int(stats[0])
            stat_bonus = int(stats[1])
            stat_value = stat_points + stat_bonus
            if отображение == "цифры":
                stat_display = f"{stat_value}" if stat_bonus == 0 else f"{stat_value} (+{stat_bonus})"
            elif отображение == "буквы":
                rank_value = max(filter(lambda x: x <= stat_value, RANKS.keys()))
                rank = RANKS.get(rank_value, "Unknown")
                stat_display = f"{rank}" if stat_bonus == 0 else f"{rank} (+{stat_bonus})"
            else:
                await ctx.send(f"Неизвестный формат отображения: {отображение}", ephemeral=True)
                return
            embed.add_field(name=f"{stat_name}:", value=stat_display)
    await ctx.send(embed=embed)

@slash_command(name="очки", description="Управляет основными очками статов персонажа", dm_permission=False)
@slash_option(
    name="member",
    description="Пользователь, статы персонажа которого вы хотите изменить",
    required=True,
    opt_type=OptionType.USER
)
@slash_option(
    name="стат",
    description="Стат, очки которой вы хотите изменить",
    required=True,
    opt_type=OptionType.STRING,
    choices=[
        SlashCommandChoice(name="Сила", value="сила"),
        SlashCommandChoice(name="Скорость", value="скорость"),
        SlashCommandChoice(name="Стойкость", value="стойкость"),
        SlashCommandChoice(name="Выносливость", value="выносливость"),
        SlashCommandChoice(name="Запас проклятой энергии", value="запас"),
        SlashCommandChoice(name="Выброс проклятой энергии", value="выброс"),
        SlashCommandChoice(name="Восприятие", value="восприятие"),
        SlashCommandChoice(name="Свойство проклятой энергии", value="свойство")
    ]
)
@slash_option(
    name="операция",
    description="Повысить или понизить очки",
    required=True,
    opt_type=OptionType.STRING,
    choices=[
        SlashCommandChoice(name="Повысить", value="повысить"),
        SlashCommandChoice(name="Понизить", value="понизить")
    ]
)
@slash_option(
    name="количество_очков",
    description="Количество очков",
    required=True,
    opt_type=OptionType.INTEGER
)
async def manage_stat_points(ctx: SlashContext, member: interactions.User, стат: str, операция: str, количество_очков: int):
    if not await check_permissions(ctx, "персонаж"):
        return
    character_folder_path = os.path.join("General", member.username, "Character")
    stats_folder_path = os.path.join("General", member.username, "Stats", "Stats")
    if not os.path.exists(character_folder_path) or not os.path.exists(stats_folder_path):
        await ctx.send(f"У пользователя {member.username} нет созданного персонажа.", ephemeral=True)
        return
    stat_file_path = os.path.join(stats_folder_path, f"{стат}.txt")
    with open(stat_file_path, "r") as f:
        stat_points, stat_bonus = map(int, f.read().strip().split("\n"))
    if операция == "повысить":
        new_stat_points = stat_points + количество_очков
    elif операция == "понизить":
        new_stat_points = max(stat_points - количество_очков, 0)
    else:
        await ctx.send(f"Неизвестная операция: {операция}", ephemeral=True)
        return
    with open(stat_file_path, "w") as f:
        f.write(f"{new_stat_points}\n{stat_bonus}")
    await ctx.send(f"{операция.capitalize()} основных очков стата {стат.capitalize()} персонажа {member.username} на {количество_очков} очков.")

@slash_command(name="бонус", description="Управляет бонусами статов персонажа", dm_permission=False)
@slash_option(
    name="member",
    description="Пользователь, бонусы статов персонажа которого вы хотите изменить",
    required=True,
    opt_type=OptionType.USER
)
@slash_option(
    name="стат",
    description="Стат, бонус которого вы хотите изменить",
    required=True,
    opt_type=OptionType.STRING,
    choices=[
        SlashCommandChoice(name="Сила", value="сила"),
        SlashCommandChoice(name="Скорость", value="скорость"),
        SlashCommandChoice(name="Стойкость", value="стойкость"),
        SlashCommandChoice(name="Выносливость", value="выносливость"),
        SlashCommandChoice(name="Запас проклятой энергии", value="запас"),
        SlashCommandChoice(name="Выброс проклятой энергии", value="выброс"),
        SlashCommandChoice(name="Восприятие", value="восприятие"),
        SlashCommandChoice(name="Свойство проклятой энергии", value="свойство")
    ]
)
@slash_option(
    name="операция",
    description="Повысить или понизить бонус",
    required=True,
    opt_type=OptionType.STRING,
    choices=[
        SlashCommandChoice(name="Повысить", value="повысить"),
        SlashCommandChoice(name="Понизить", value="понизить")
    ]
)
@slash_option(
    name="количество_бонуса",
    description="Количество бонуса",
    required=True,
    opt_type=OptionType.INTEGER
)
async def manage_stat_bonus(ctx: SlashContext, member: interactions.User, стат: str, операция: str, количество_бонуса: int):
    if not await check_permissions(ctx, "персонаж"):
        return
    character_folder_path = os.path.join("General", member.username, "Character")
    stats_folder_path = os.path.join("General", member.username, "Stats", "Stats")
    if not os.path.exists(character_folder_path) or not os.path.exists(stats_folder_path):
        await ctx.send(f"У пользователя {member.username} нет созданного персонажа.", ephemeral=True)
        return
    stat_file_path = os.path.join(stats_folder_path, f"{стат}.txt")
    with open(stat_file_path, "r") as f:
        stat_points, stat_bonus = map(int, f.read().strip().split("\n"))
    if операция == "повысить":
        new_stat_bonus = stat_bonus + количество_бонуса
    elif операция == "понизить":
        new_stat_bonus = max(stat_bonus - количество_бонуса, 0)
    else:
        await ctx.send(f"Неизвестная операция: {операция}", ephemeral=True)
        return
    with open(stat_file_path, "w") as f:
        f.write(f"{stat_points}\n{new_stat_bonus}")
    await ctx.send(f"{операция.capitalize()} бонуса стата {стат.capitalize()} персонажа {member.username} на {количество_бонуса} очков.")

@slash_command(name="техники", description="Показывает информацию о техниках персонажа")
@slash_option(
    name="member",
    description="Пользователь, техники которого вы хотите увидеть",
    required=False,
    opt_type=OptionType.USER
)
async def show_techniques(ctx: SlashContext, member: interactions.User = None):
    if member is None:
        member = ctx.author
    techniques_folder_path = os.path.join('General', member.username, 'Stats', 'Techniques')
    if not os.path.exists(techniques_folder_path):
        await ctx.send(f"У пользователя {member.username} нет информации о техниках.", ephemeral=True)
        return
    with open(os.path.join("General", member.username, "Character", "имя.txt"), "r") as f:
        first_name = f.read()
    with open(os.path.join("General", member.username, "Character", "фамилия.txt"), "r") as f:
        last_name = f.read()
    embed = interactions.Embed(
        color=0xFF9933
    )
    embed.set_author(name=f"{member.username}", icon_url=member.avatar_url)
    embed.title = f"{first_name} {last_name}"
    techniques_dict = {
        "барьеры.txt": "Барьеры",
        "РТ.txt": "Расширение территорий",
        "ОПТ.txt": "Обратная проклятая техника",
        "ПТ.txt": "Простая территория",
        "РП.txt": "Растяжение пространства",
        "Эмоция.txt": "Эмоция падающего цветка",
        "Корзина.txt": "Сплетение абсолютной пустоты",
        "ЧМ.txt": "Черная молния",
    }
    for technique_file, technique_name in techniques_dict.items():
        with open(os.path.join(techniques_folder_path, technique_file), "r") as f:
            mastery_level = int(f.read().strip())
            mastery_text = TECHNIQUE_LIBRARIES.get(mastery_level, "Некорректный уровень владения")
            embed.add_field(name=technique_name, value=mastery_text, inline=False)
    await ctx.send(embed=embed)

@slash_command(name="техника", description="Изменяет уровень владения техникой", dm_permission=False)
@slash_option(
    name="member",
    description="Пользователь, технику которого нужно изменить",
    required=True,
    opt_type=OptionType.USER
)
@slash_option(
    name="техника",
    description="Выберите технику для изменения",
    required=True,
    opt_type=OptionType.STRING,
    choices=[
        SlashCommandChoice(name="Расширение территорий", value="РТ"),
        SlashCommandChoice(name="Простая территория", value="ПТ"),
        SlashCommandChoice(name="Обратная проклятая техника", value="ОПТ"),
        SlashCommandChoice(name="Барьеры", value="Барьеры"),
        SlashCommandChoice(name="Черная молния", value="ЧМ"),
        SlashCommandChoice(name="Растяжение пространства", value="РП"),
        SlashCommandChoice(name="Эмоция падающего цветка", value="Эмоция"),
        SlashCommandChoice(name="Сплетение абсолютной пустоты", value="Корзина")
    ]
)
@slash_option(
    name="новое_значение",
    description="Новый уровень владения техникой (от 0 до 4)",
    required=True,
    opt_type=OptionType.INTEGER,
    min_value=0,
    max_value=4
)
async def manage_technique(ctx: SlashContext, member: interactions.User, техника: str, новое_значение: int):
    if not await check_permissions(ctx, "персонаж"):
        return
    techniques_folder_path = os.path.join('General', member.username, 'Stats', 'Techniques')
    if not os.path.exists(techniques_folder_path):
        await ctx.send(f"У пользователя {member.username} нет информации о техниках.", ephemeral=True)
        return
    technique_files = {
        "РТ": "РТ.txt",
        "ЧМ": "ЧМ.txt",
        "ПТ": "ПТ.txt",
        "ОПТ": "ОПТ.txt",
        "Барьеры": "барьеры.txt",
        "Эмоция": "Эмоция.txt",
        "Корзина": "Корзина.txt",
        "РП": "РП.txt"
    }
    technique_file = technique_files.get(техника)
    if not technique_file:
        await ctx.send("Некорректная техника.", ephemeral=True)
        return
    technique_path = os.path.join(techniques_folder_path, technique_file)
    with open(technique_path, "w") as f:
        f.write(str(новое_значение))
    await ctx.send(f"Уровень владения техникой '{техника}' для пользователя {member.username} изменен на {новое_значение}.")

@slash_command(name="баланс", description="Показывает текущий баланс кошелька")
@slash_option(
    name="member",
    description="Пользователь, баланс которого нужно посмотреть",
    required=False,
    opt_type=OptionType.USER
)
async def wallet_balance(ctx: SlashContext, member: interactions.User = None):
    if not member:
        member = ctx.author
    wallet_file_path = os.path.join('General', member.username, 'Inventory', 'wallet.txt')
    if not os.path.exists(wallet_file_path):
        await ctx.send(f"У пользователя {member.username} нет кошелька.", ephemeral=True)
        return
    with open(wallet_file_path, "r") as f:
        balance = int(f.read())
    with open(os.path.join("General", member.username, "Character", "имя.txt"), "r") as f:
        first_name = f.read()
    with open(os.path.join("General", member.username, "Character", "фамилия.txt"), "r") as f:
        last_name = f.read()
    embed = interactions.Embed(
        color=0xFF9933
    )
    embed.set_author(name=f"{member.username}", icon_url=member.avatar_url)
    embed.title = f"{first_name} {last_name}"
    with open(wallet_file_path) as f:
        balance = int(f.read())
    with open(os.path.join(wallet_file_path), "r") as f:
        embed.add_field(name="Баланс", value=f"{balance}¥", inline=False)
    await ctx.send(embed=embed)

@slash_command(name="зарплата", description="Изменение баланса пользователя", dm_permission=False)
@slash_option(
    name="member",
    description="Пользователь, баланс которого нужно изменить",
    required=True,
    opt_type=OptionType.USER
)
@slash_option(
    name="операция",
    description="Повысить или понизить баланс",
    required=True,
    opt_type=OptionType.STRING,
    choices=[
        SlashCommandChoice(name="повысить", value="Повысить"),
        SlashCommandChoice(name="понизить", value="Понизить")
    ]
)
@slash_option(
    name="количество",
    description="Сумма, на которую нужно изменить баланс",
    required=True,
    opt_type=OptionType.INTEGER
)
async def manage_wallet_balance(ctx: SlashContext, member: interactions.User, операция: str, количество: int):
    if not await check_permissions(ctx, "инвентарь"):
        return
    wallet_file_path = os.path.join('General', member.username, 'Inventory', 'wallet.txt')
    if not os.path.exists(wallet_file_path):
        await ctx.send(f"У пользователя {member.username} нет кошелька.", ephemeral=True)
        return
    with open(wallet_file_path, "r") as f:
        balance = int(f.read())
    if операция == "Повысить":
        new_balance = balance + количество
    else:
        new_balance = balance - количество
    with open(wallet_file_path, "w") as f:
        f.write(str(new_balance))
    await ctx.send(f"Баланс был {'повышен' if операция == 'Повысить' else 'понижен'} на {количество} ¥")

@slash_command(name="купить", description="Купить предмет", dm_permission=False)
@slash_option(
    name="название_товара",
    description="Название товара",
    required=True,
    opt_type=OptionType.STRING
)
@slash_option(
    name="количество",
    description="Количество товара",
    required=True,
    opt_type=OptionType.INTEGER
)
@slash_option(
    name="стоимость",
    description="Стоимость товара (за штуку)",
    required=True,
    opt_type=OptionType.INTEGER
)
async def buy(ctx: SlashContext, название_товара: str, количество: int, стоимость: int):
    wallet_file_path = os.path.join('General', ctx.author.username, 'Inventory', 'wallet.txt')
    if not os.path.exists(wallet_file_path):
        await ctx.send(f"У пользователя {ctx.author.username} нет кошелька.", ephemeral=True)
        return
    with open(wallet_file_path, "r") as f:
        balance = int(f.read())
    total_cost = стоимость * количество
    if balance < total_cost:
        await ctx.send(f"У вас недостаточно средств для покупки {количество} шт. {название_товара} за {total_cost} ¥.", ephemeral=True)
        return
    new_balance = balance - total_cost
    with open(wallet_file_path, "w") as f:
        f.write(str(new_balance))
    item_file_path = os.path.join('General', ctx.author.username, 'Inventory', "Items", f"{название_товара}.txt")
    if not os.path.exists(item_file_path):
        with open(item_file_path, "w") as f:
            f.write(str(количество))
    else:
        with open(item_file_path, "r") as f:
            current_quantity = int(f.read())
        new_quantity = current_quantity + количество
        with open(item_file_path, "w") as f:
            f.write(str(new_quantity))
    embed = interactions.Embed(
        title="Покупка выполнена",
        description=f"Вы купили {количество} шт. {название_товара} за {total_cost} ¥.",
        color=0xFF9933
    )
    embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
    embed.add_field(name="Новый баланс", value=f"{new_balance} ¥", inline=False)
    await ctx.send(embed=embed)

@slash_command(name="инвентарь", description="Посмотреть инвентарь")
@slash_option(
    name="member",
    description="Просмотреть инвентарь другого пользователя",
    required=False,
    opt_type=OptionType.USER
)
async def view_inventory(ctx: SlashContext, member: interactions.Member = None):
    if not member:
        member = ctx.author
    inventory_folder_path = os.path.join('General', member.username, 'Inventory', 'Items')
    if not os.path.exists(inventory_folder_path):
        await ctx.send(f"У пользователя {member.mention} нет персонажа.", ephemeral=True)
        return
    item_files = os.listdir(inventory_folder_path)
    with open(os.path.join("General", member.username, "Character", "имя.txt"), "r") as f:
        first_name = f.read()
    with open(os.path.join("General", member.username, "Character", "фамилия.txt"), "r") as f:
        last_name = f.read()
    embed = interactions.Embed(
        color=0xFF9933
    )
    embed.set_author(name=f"{member.username}", icon_url=member.avatar_url)
    embed.title = f"{first_name} {last_name}"
    for item_file in item_files:
        item_name = os.path.splitext(item_file)[0]
        item_file_path = os.path.join(inventory_folder_path, item_file)
        with open(item_file_path, "r") as f:
            item_quantity = int(f.read())
        embed.add_field(name=item_name, value=f"Количество: {item_quantity} штук", inline=False)
    await ctx.send(embed=embed)

@slash_command(name="выдать", description="Выдать или забрать предмет", dm_permission=False)
@slash_option(
    name="пользователь",
    description="Пользователь, которому будет выдан/забран предмет",
    required=True,
    opt_type=OptionType.USER
)
@slash_option(
    name="действие",
    description="Выдать или забрать предмет",
    required=True,
    opt_type=OptionType.STRING,
    choices=[
        SlashCommandChoice(name="Выдать", value="выдать"),
        SlashCommandChoice(name="Забрать", value="забрать")
    ]
)
@slash_option(
    name="название_предмета",
    description="Название предмета",
    required=True,
    opt_type=OptionType.STRING
)
@slash_option(
    name="количество",
    description="Количество предмета",
    required=True,
    opt_type=OptionType.INTEGER
)
async def manage_items(ctx:SlashContext,пользователь:interactions.Member, действие: str, название_предмета: str, количество: int):
    if not await check_permissions(ctx, "инвентарь"):
        return
    inventory_folder_path = os.path.join('General', пользователь.username, 'Inventory', 'Items')
    item_file_path = os.path.join(inventory_folder_path, f"{название_предмета}.txt")
    if os.path.exists(item_file_path):
        with open(item_file_path, "r") as f:
            current_quantity = int(f.read())
    else:
        current_quantity = 0
    if действие == "выдать":
        if not os.path.exists(item_file_path):
            with open(item_file_path, "w") as f:
                f.write(str(0))
        new_quantity = current_quantity + количество
        with open(item_file_path, "w") as f:
            f.write(str(new_quantity))
        await ctx.send(f"Пользователю {пользователь.display_name} выдано {количество} шт. {название_предмета}.")
    elif действие == "забрать":
        if current_quantity < количество:
            await ctx.send(f"У пользователя {пользователь.display_name} недостаточно предметов '{название_предмета}' для удаления.", ephemeral=True)
            return
        new_quantity = current_quantity - количество
        if new_quantity == 0:
            os.remove(item_file_path)
            await ctx.send(f"У пользователя {пользователь.display_name} забрано {количество} шт. {название_предмета}. Предмет удален из инвентаря.")
        else:
            with open(item_file_path, "w") as f:
                f.write(str(new_quantity))
            await ctx.send(f"У пользователя {пользователь.display_name} забрано {количество} шт. {название_предмета}.")

@slash_command(name="использовать", description="Использовать определенное количество предметов из инвентаря", dm_permission=False)
@slash_option(
    name="название_предмета",
    description="Название предмета для использования",
    required=True,
    opt_type=OptionType.STRING
)
@slash_option(
    name="количество",
    description="Количество предметов для использования",
    required=False,
    opt_type=OptionType.INTEGER
)
async def use_item(ctx: SlashContext, название_предмета: str, количество: int = 1):
    if not количество:
        количество = 1

    # Получить путь к папке инвентаря пользователя
    inventory_folder_path = os.path.join('General', ctx.author.username, 'Inventory', 'Items')

    # Получить путь к файлу предмета
    item_file_path = os.path.join(inventory_folder_path, f"{название_предмета}.txt")

    # Проверить, существует ли файл предмета
    if os.path.exists(item_file_path):
        # Прочитать текущее количество предмета
        with open(item_file_path, 'r') as f:
            current_quantity = int(f.read())

        # Проверить, достаточно ли предметов для использования
        if current_quantity >= количество:
            # Вычитаем использованное количество предметов
            new_quantity = current_quantity - количество

            # Обновляем количество предметов в файле
            with open(item_file_path, 'w') as f:
                f.write(str(new_quantity))

            # Проверяем, стало ли количество предмета равным 0
            if new_quantity == 0:
                # Удаляем файл предмета
                os.remove(item_file_path)
                await ctx.send(f"Из инвентаря использовано {количество} шт. предмета '{название_предмета}'.")
            else:
                await ctx.send(f"Из инвентаря использовано {количество} шт. предмета '{название_предмета}'.")
        else:
            await ctx.send(f"У вас недостаточно предметов '{название_предмета}' для использования.", ephemeral=True)
    else:
        await ctx.send(f"У вас нет предмета '{название_предмета}' в инвентаре.", ephemeral=True)

@slash_command(name="передать", description="Передать предмет другому игроку", dm_permission=False)
@slash_option(
    name="пинг",
    description="Пинг пользователя, которому нужно передать предмет",
    required=True,
    opt_type=OptionType.USER
)
@slash_option(
    name="название_предмета",
    description="Название предмета для передачи",
    required=True,
    opt_type=OptionType.STRING
)
@slash_option(
    name="количество",
    description="Количество предметов для передачи (необязательно)",
    required=False,
    opt_type=OptionType.INTEGER
)
async def transfer_item(ctx: SlashContext, пинг: interactions.User, название_предмета: str, количество: int = 1):
    # Получить путь к папке инвентаря пользователя, отправившего команду
    sender_inventory_folder_path = os.path.join('General', ctx.author.username, 'Inventory', 'Items')
    # Получить путь к папке инвентаря пользователя, которому передают предмет
    receiver_inventory_folder_path = os.path.join('General', пинг.username, 'Inventory', 'Items')

    # Проверить, достаточно ли предметов у отправителя
    sender_item_file_path = os.path.join(sender_inventory_folder_path, f"{название_предмета}.txt")
    if os.path.exists(sender_item_file_path):
        with open(sender_item_file_path, 'r') as f:
            sender_current_quantity = int(f.read())
        if sender_current_quantity >= количество:
            # Вычитаем переданное количество предметов из инвентаря отправителя
            sender_new_quantity = sender_current_quantity - количество
            with open(sender_item_file_path, 'w') as f:
                f.write(str(sender_new_quantity))
            
            # Если после передачи количество предметов у отправителя стало 0, удаляем файл
            if sender_new_quantity == 0:
                os.remove(sender_item_file_path)

            # Добавляем переданные предметы в инвентарь получателя
            receiver_item_file_path = os.path.join(receiver_inventory_folder_path, f"{название_предмета}.txt")
            if os.path.exists(receiver_item_file_path):
                with open(receiver_item_file_path, 'r') as f:
                    receiver_current_quantity = int(f.read())
                receiver_new_quantity = receiver_current_quantity + количество
                with open(receiver_item_file_path, 'w') as f:
                    f.write(str(receiver_new_quantity))
            else:
                with open(receiver_item_file_path, 'w') as f:
                    f.write(str(количество))

            await ctx.send(f"{ctx.author.user.username} передал {количество} шт. предмета '{название_предмета}' пользователю {пинг.username}.")
        else:
            await ctx.send(f"У вас недостаточно предметов '{название_предмета}' для передачи.", ephemeral=True)
    else:
        await ctx.send(f"У вас нет предмета '{название_предмета}' в инвентаре.", ephemeral=True)

@slash_command(name="заплатить", description="Передать деньги другому игроку", dm_permission=False)
@slash_option(
    name="пинг",
    description="Пинг пользователя, которому нужно перевести деньги",
    required=True,
    opt_type=OptionType.USER
)
@slash_option(
    name="количество",
    description="Количество денег для перевода",
    required=True,
    opt_type=OptionType.INTEGER
)
async def pay(ctx: SlashContext, пинг: interactions.User, количество: int):
    # Получить путь к папке "Деньги" пользователя, отправившего команду
    sender_money_folder_path = os.path.join('General', ctx.author.username, 'Inventory', "wallet.txt")
    # Получить путь к папке "Деньги" пользователя, которому переводят деньги
    receiver_money_folder_path = os.path.join('General', пинг.username, 'Inventory', "wallet.txt")

    # Проверить, достаточно ли денег у отправителя
    sender_money_file_path = os.path.join(sender_money_folder_path)

    if os.path.exists(sender_money_file_path):
        with open(sender_money_file_path, 'r') as f:
            sender_current_money = int(f.read())
        if sender_current_money >= количество:
            # Вычитаем переданную сумму из денег отправителя
            sender_new_money = sender_current_money - количество
            with open(sender_money_file_path, 'w') as f:
                f.write(str(sender_new_money))

            # Добавляем переданную сумму к деньгам получателя
            receiver_money_file_path = os.path.join(receiver_money_folder_path)
            if os.path.exists(receiver_money_file_path):
                with open(receiver_money_file_path, 'r') as f:
                    receiver_current_money = int(f.read())
                receiver_new_money = receiver_current_money + количество
                with open(receiver_money_file_path, 'w') as f:
                    f.write(str(receiver_new_money))
            else:
                with open(receiver_money_file_path, 'w') as f:
                    f.write(str(количество))

            await ctx.send(f"{ctx.author.user.username} перевел {количество} денег пользователю {пинг.username}.")
        else:
            await ctx.send(f"У вас недостаточно денег для перевода.", ephemeral=True)
    else:
        await ctx.send(f"У вас нет денег.", ephemeral=True)
