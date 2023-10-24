import logging
import json

from bot import bot

from urllib3 import disable_warnings
from urllib3.exceptions import InsecureRequestWarning

# root logger has timestamp, module name, level and message
logging.basicConfig(
    format="%(asctime)s %(name)s %(levelname)s %(message)s", level=logging.INFO
)


if __name__ == "__main__":
    with open("token.json", "r", encoding="utf8") as f:
        json = json.load(f)
    bot.run(json["token"])
