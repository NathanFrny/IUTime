import datetime
import logging
import asyncio
from functools import partial
from discord import (
    Embed,
    Intents,
    Member,
    User,
    Bot,
    ApplicationContext,
    Guild,
    Role,
    InteractionResponded,
    Option,
)
from discord.ext import tasks
from request import lessons_tp
from utils import (
    notification_parameter_change,
    get_notified_users,
    schedule_task,
    add_homework_for_tp,
    homework_for_tp,
    del_homework_for_tp,
    homework_auto_remove,
)
from constants import (
    TOKEN,
    TP_DISCORD_TO_SCHEDULE,
    DATASOURCES,
    IUTSERVID,
    ZINCEID,
    NOTIFICATION_JSON_KEYS,
    HOMEWORKSOURCES,
    TP_SCHEDULE_TO_DISCORD,
    TARGETED_HOUR,
)
from homework import Homework
from lesson import Lesson

intents = Intents.default()
bot: Bot = Bot(intents=intents)


@bot.event
async def on_ready():
    """Actions to do when the bot is ready to use"""
    if not bot.user:
        raise InterruptedError("The bot didn't connect")

    logging.info(
        "Logged in as %s (%s)", bot.user.name, bot.user.id
    )  # Bot connection confirmation
    await wait_for_start_time()


@tasks.loop(hours=24)
async def plan_notif_for_tp():
    """For each tp, create a list of sorted lesson, will this list is not empty, plan a notification for the next lesson"""
    all_lesson: list = []
    for (
        t_p
    ) in TP_DISCORD_TO_SCHEDULE.keys():  # pylint: disable=consider-iterating-dictionary
        schedule_: list[Lesson] = lessons_tp(t_p=TP_DISCORD_TO_SCHEDULE[t_p])
        for lesson in schedule_:
            all_lesson.append(lesson)

    all_lesson = Lesson.sorting_schedule(all_lesson)
    while all_lesson != []:
        lesson = all_lesson.pop(0)
        logging.debug("lesson = %s", lesson)
        await plan_notification(t_p=TP_SCHEDULE_TO_DISCORD[lesson.t_p], lesson=lesson)


@tasks.loop(hours=24)
async def homeworks_notif():
    """Send a notification of homeworks for each users who activate notifications
    and delete out-dated homeworks"""
    homework_dict: dict = {}
    for t_p in TP_DISCORD_TO_SCHEDULE.keys():
        homeworks = homework_for_tp(TP_DISCORD_TO_SCHEDULE[t_p])
        homework_dict[t_p] = Homework.embed_homework_construct(
            title="automatic notifications homeworks",
            color=0x00FF00,
            homeworks=homeworks,
            description=f"Homeworks for {TP_DISCORD_TO_SCHEDULE[t_p]}",
            sign=True,
            sorting=True,
        )
    for t_p in homework_dict.keys():
        users_list = await get_user_list_from_tp(notify="homeworks", t_p=t_p)
        await send_notification(user_list=users_list, embed=homework_dict[t_p])

    homework_auto_remove()


@bot.command(description="Ask your schedule")
async def schedule(ctx: ApplicationContext, t_p: Option(str, description="TP group")):
    """Command to retrieve and send the schedule for a specific TP group.
        If hour > 19, retrieve and send tommorow's shedule

    Args:
        ctx (ApplicationContext): The application context.
        t_p (str): The TP group for which to retrieve the schedule.
    """
    user: User | Member = ctx.author
    logging.debug("User value : %s", user)
    if t_p.upper() in TP_DISCORD_TO_SCHEDULE.values():
        logging.debug("tp value : %s", t_p)
        date: datetime.datetime = datetime.datetime.now()
        logging.debug("date = %s", date)
        if date.hour >= 19:
            tomorrow: bool = True
            date += datetime.timedelta(days=1)
        else:
            tomorrow: bool = False
        _schedule: list = Lesson.sorting_schedule(lessons_tp(t_p, tomorrow=tomorrow))
        logging.debug("schedule value : %s", _schedule)

        embed = Lesson.embed_schedule_construct(
            title=f"Emploi du temps du {date.day}/{date.month}/{date.year}",
            description=f"{t_p}",
            color=0xFF0000,  # red
            schedule=_schedule,
            sign=True,
        )

        await send_notification(user_list=[user], embed=embed)
        await ctx.interaction.response.send_message("Done!")  # Responding to user
    else:
        logging.debug("TP not found")
        message: str = "Les arguments attendus sont :"
        for element in TP_DISCORD_TO_SCHEDULE.values():
            message += element + ", "
        message = message[:-2]  # Last 2 caracters suppression
        await ctx.interaction.response.send_message(
            message
        )  # Responding if bad argument


@bot.command(description="Able/Enable notifications for homeworks or lessons")
async def notif(
    ctx: ApplicationContext,
    notification: Option(str, description="Notification parameter you want to change"),
    boolean: Option(bool, description="True if you want the notification, False else"),
):
    """Enable users to change their notification parameters

    Args:
        ctx (ApplicationContext): Discord users recuperation
        notification (str): which notification need to change
        boolean (bool): True if notification desired, False else
    """
    if notification in NOTIFICATION_JSON_KEYS:
        author_id: str = str(ctx.author.id)
        result = notification_parameter_change(
            user_id=author_id,
            parameter=boolean,
            notification=notification,
            path=DATASOURCES,
        )
        if result:
            await ctx.interaction.response.send_message("Done!")
        else:
            # Never supposed to appear
            zince: User = await bot.fetch_user(ZINCEID)
            date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
            await zince.send(
                f"({date}) Error in notif function (main.py) for user\
                    {ctx.author}, notification = {notification}, boolean = {boolean}"
            )
            await ctx.interaction.response.send_message(
                "An error happened, my creators have been notified"
            )
    else:
        logging.debug("Notification not found")
        message: str = "Les arguments attendus sont: "
        for element in NOTIFICATION_JSON_KEYS:
            message += element + ", "
        message = message[:-2]  # Last 2 caracters suppression
        await ctx.interaction.response.send_message(
            message
        )  # Responding if bad argument


@bot.command(description="Ask recorded homeworks for your TP")
async def homework(ctx: ApplicationContext):
    """Command to retrieve and send homeworks to the user.

    Args:
        ctx (ApplicationContext): The application context.
    """
    user: User | Member = ctx.author
    homeworks: list = None
    logging.debug("User value : %s", user)
    # User's TP recuperation
    roles: list[Role] = user.roles
    for role in roles:
        logging.debug("role value : %s", role)
        if role.name in TP_DISCORD_TO_SCHEDULE.keys():
            logging.debug("role.name value : %s", role.name)
            homeworks_temp: list[Homework] = homework_for_tp(
                TP_DISCORD_TO_SCHEDULE[role.name], path=HOMEWORKSOURCES
            )
            logging.debug("homeworks_temp value : %s", homeworks_temp)
            logging.debug(
                "homeworks_temp's elem type : %s",
                {
                    type(homeworks_temp[0])
                    if homeworks_temp
                    else "homeworks_temp is empty"
                },
            )
            homeworks: list[Homework] = []
            # DO NOT use remove method here
            for homework_ in homeworks_temp:
                if homework_.criticite_compare():
                    homeworks.append(homework_)
            # Sending homeworks or another message if not homeworks
            if homeworks:
                embed: Embed = Homework.embed_homework_construct(
                    title=role.name,
                    color=0x00FF00,
                    homeworks=homeworks,
                    description="Homeworks",
                )
                await send_notification(user_list=[user], embed=embed)
                await ctx.interaction.response.send_message("Done!")
            else:
                await send_notification(
                    user_list=[user], message="No homeworks recorded"
                )
                await ctx.interaction.response.send_message("Done!")
            break

    # If user has not any TP group
    try:
        await ctx.interaction.response.send_message(
            "No TP group assigned to you on this discord server"
        )
    except InteractionResponded:
        pass


@bot.command(description="Add an homework to your TP")
async def add_homework(
    ctx: ApplicationContext,
    ressource: Option(str, description="Ressource of the homework"),
    prof: Option(str, description="For which teacher"),
    criticite: Option(
        str,
        description="Importance, 'banale' to be notified 1 day before, 'normal' for 3 days, 'critique' to always be",
    ),
    date_rendu: Option(str, description="Due date, exemple '2023-07-03-02-40"),
    description: Option(str, description="A simple desciption of the homework"),
    note: Option(bool, description="If graded or not") = False,
):
    """Command to add a homework to the TP.

    Args:
        ctx (ApplicationContext): The application context.
        ressource (str): The resource of the homework.
        prof (str): The professor of the homework.
        criticite (str): The importance/criticality of the homework.
        date_rendu (str): The deadline of the homework in the format 'YYYY-MM-DD-HH-MM'.
        description (str): The description of the homework.
        note (bool, optional): Whether the homework needs to be noted. Defaults to False.
    """

    user: User | Member = ctx.author
    roles: list[Role] = user.roles
    roles_name: list[str] = []
    for role in roles:
        roles_name.append(role.name)

    logging.debug("roles_name = %s", roles_name)

    for name in roles_name:
        if name in TP_DISCORD_TO_SCHEDULE.keys() and "délégué" in roles_name:
            logging.debug("TP and role 'délégué' found")
            try:
                date_rendu_obj: datetime.datetime = datetime.datetime.strptime(
                    date_rendu, "%Y-%m-%d-%H-%M"
                )
            except ValueError:
                await ctx.interaction.response.send_message(
                    "Invalid date format. Use the format 'YYYY-MM-DD-HH-MM'"
                )
                return

            homework_ = Homework(
                ressource, prof, criticite, date_rendu_obj, description, note
            )
            logging.debug("homework = %s", homework_)
            result: bool = add_homework_for_tp(
                homework=homework_,
                t_p=TP_DISCORD_TO_SCHEDULE[name],
                path=HOMEWORKSOURCES,
            )
            if result:
                await ctx.interaction.response.send_message("Homework added!")
            else:
                # Never supposed to appear
                zince: User = await bot.fetch_user(ZINCEID)
                date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
                await zince.send(
                    f"({date}) Error in add_homework function (main.py)\
for user {ctx.author}, tp = {name}, homework = {homework_}"
                )
                await ctx.interaction.response.send_message(
                    "An error happened, my creators have been notified"
                )
            break
    try:
        logging.debug("TP or role 'délégué' not found")
        await ctx.interaction.response.send_message(
            "Only TP delegates have the right to modify recorded homeworks"
        )
    except InteractionResponded:
        pass


@bot.command(description="Delete an homework to your TP")
async def del_homework(
    ctx: ApplicationContext,
    emplacement: Option(
        int,
        description="Homework's list placement, start to 1, let empty to obtain the list of homeworks",
    ) = None,
):
    """Command to delete a homework from the TP.

    Args:
        ctx (ApplicationContext): The application context.
        emplacement (int, optional): The placement of the homework to be deleted. Defaults to None.
    """
    user: User | Member = ctx.author
    roles: list[Role] = user.roles
    roles_name: list[str] = []
    for role in roles:
        roles_name.append(role.name)

    logging.debug("roles_name = %s", roles_name)

    for name in roles_name:
        if name in TP_DISCORD_TO_SCHEDULE.keys() and "délégué" in roles_name:
            # 0 = not
            if not emplacement:
                logging.debug("not placement")

                homeworks: list[Homework] = homework_for_tp(
                    t_p=TP_DISCORD_TO_SCHEDULE[name], path=HOMEWORKSOURCES
                )
                logging.debug("homeworks = %s", homeworks)
                embed: Embed = Homework.embed_homework_construct(
                    title="Homeworks recorded list",
                    description="Use the /del_homework command, indicating\
the number of the homework you want to delete",
                    color=0x00FF00,
                    homeworks=homeworks,
                    sorting=False,
                )
                await ctx.interaction.response.send_message(embed=embed)
            else:
                logging.debug("placement")
                result: int = del_homework_for_tp(
                    placement=emplacement - 1,
                    t_p=TP_DISCORD_TO_SCHEDULE[name],
                    path=HOMEWORKSOURCES,
                )
                match result:
                    case 1:
                        await ctx.interaction.response.send_message("Done!")
                    case 0:
                        # Never supposed to appear
                        zince: User = await bot.fetch_user(ZINCEID)
                        date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
                        await zince.send(
                            f"({date}) Error in del_homework function (main.py) for\
user {ctx.author}, tp = {name}, placement = {emplacement}"
                        )
                        await ctx.interaction.response.send_message(
                            "An error happened, my creators have been notified"
                        )
                    case 2:
                        await ctx.interaction.response.send_message(
                            "Seems like this homework doesn't exist"
                        )
                break
    try:
        await ctx.interaction.response.send_message(
            "Only TP delegates have the right to modify recorded homeworks"
        )
    except InteractionResponded:
        pass


async def plan_notification(t_p: str, lesson: Lesson) -> None:
    """Send a notification 5 minutes before the next lesson

    Args:
        tp (str): code of the TP group
        lesson (lesson): lesson object that should be sent
    """
    logging.debug("Send lesson for TP %s : %s", t_p, lesson)

    embed: Embed = Lesson.embed_schedule_construct(
        title="Next lesson:",
        description=None,
        color=0x9370DB,
        schedule=[lesson],
        sign=True,
    )
    lesson_time: datetime.datetime = datetime.datetime.strptime(
        lesson.start_hour, "%H:%M"
    ).time()
    lesson_time: datetime.datetime = datetime.datetime.combine(
        datetime.date.today(), lesson_time
    )
    if lesson_time < datetime.datetime.now() - datetime.timedelta(hours=1, minutes=30):
        logging.info("Lesson time to far in the past, %s", lesson_time)
        return

    notification_time: datetime.datetime = datetime.datetime.now()
    notification_time = notification_time.replace(
        hour=lesson_time.hour, minute=lesson_time.minute
    )
    # notification sent 5 min before lesson
    notification_time -= datetime.timedelta(minutes=5)

    task = partial(
        send_notification,
        await get_user_list_from_tp(notify="next_lesson", t_p=t_p),
        embed=embed,
    )

    await schedule_task(
        task,
        notification_time,
    )


async def send_notification(
    user_list: list[User], embed: Embed = None, message: str = None
):
    """Sends a notification with a private message to all the users in user_list

    Args:
        user_list (list[User]): The list of users to be notified
        embed (Embed | None): The embed that will be sent
        message (str | None): The message that will be sent
    """

    for user in user_list:
        if message:
            await user.send(message)
        if embed:
            await user.send(embed=embed)
    logging.debug("notification sent to users : %s", user_list)


async def get_user_list_from_tp(notify: str, t_p: str, serv_id=IUTSERVID) -> list:
    """Return a list of user's ID who activated the notification searched

    Args:
        notify (str):notification searched
        tp (str): TP group (exemple: BUT1-TPA)
        serv_id (int): targeted server. DEFAULT IUTSERVID

    Returns:
        list: users discord ID
    """
    logging.debug("t_p =  %s", t_p)
    res = []
    user_list: list[str] = get_notified_users(notify=notify)
    guild: Guild = bot.get_guild(serv_id)
    logging.debug("Discord server found: %s", guild.name)
    if guild:
        for user_ in user_list:
            logging.debug("user_ = %s", user_)
            member: Member = await guild.fetch_member(user_)
            logging.debug("member = %s", member)
            roles = member.roles
            logging.debug("roles = %s", roles)
            for role in roles:
                if t_p == role.name:
                    res.append(member)
    else:
        raise RuntimeError("Discord server not found")

    return res


async def wait_for_start_time():
    current_time: datetime.datetime = datetime.datetime.now()
    target_time: datetime.datetime = datetime.datetime(
        current_time.year,
        current_time.month,
        current_time.day,
        TARGETED_HOUR[0],
        TARGETED_HOUR[1],
    )
    logging.debug("target time = %s", target_time)
    # Calculate delay before target time
    if current_time < target_time:
        wait_time: datetime = target_time - current_time
        logging.debug("wait time = %s", wait_time)
    else:
        next_day: datetime.datetime = current_time + datetime.timedelta(days=1)
        target_time = datetime.datetime(
            next_day.year,
            next_day.month,
            next_day.day,
            TARGETED_HOUR[0],
            TARGETED_HOUR[1],
        )
        wait_time: datetime.timedelta = target_time - current_time

    # waiting until target time
    logging.info("waiting %s seconds", wait_time.total_seconds())
    await asyncio.sleep(wait_time.total_seconds())

    asyncio.ensure_future(plan_notif_for_tp.start())

    await asyncio.sleep(
        58200
    )  # 16 hours and 10 min (if plan_notif start at 3am, homeworks are sent around 7pm10)
    asyncio.ensure_future(homeworks_notif.start())


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s | %(levelname)s | %(filename)s | %(funcName)s : %(message)s",
    )
    bot.run(TOKEN)
