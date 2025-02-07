import os
import time
from parser import parse_link
from playwright.sync_api import TimeoutError
from discord_webhook import DiscordEmbed, DiscordWebhook
import logging
from downloader import full_download

# GLOBAL_DISCORD_TIMEOUT = 5
GLOBAL_CHECKER_TIMEOUT = 60 * 60
GLOBAL_SLEEP = 1
GLOBAL_MANGA_PATH = "download"
GLOBAL_SEEN_DATA = "seen.txt"
GLOBAL_COMIC_LIST = "manga.txt"
GLOBAL_DISCORD_WEBHOOK = "discord.txt"

logging.basicConfig(
    filename="log.log",
    encoding="utf-8",
    filemode="a",
    format="{asctime} - {levelname} - {message}",
    style="{",
    datefmt="%Y-%m-%d %H:%M:%S",
    level=logging.INFO
)

def send_message(
    embed_title: str = "New Manga Chapter downloaded",
    embed_url: str | None = None,
    embed_content: str | None = None,
):
    if not os.path.exists(GLOBAL_DISCORD_WEBHOOK):
        return
    with open(GLOBAL_DISCORD_WEBHOOK, "r") as f:
        link = f.read().strip()
    if len(link)<10:
        return
    wb = DiscordWebhook(
        url=link,
    )
    embed = DiscordEmbed(title=embed_title, url=embed_url, description=embed_content)
    wb.add_embed(embed)
    _ = wb.execute()


def get_chapter_id(link: str):
    return link.split("/")[-1]


def main():
    if not os.path.exists(GLOBAL_MANGA_PATH):
        os.mkdir(GLOBAL_MANGA_PATH)
    if not os.path.exists(GLOBAL_COMIC_LIST):
        logging.error("Please provide a mangalist, every line should contain 1 link")
        exit()
    while True:
        seen_ids = []
        if os.path.exists(GLOBAL_SEEN_DATA):
            with open(GLOBAL_SEEN_DATA, "r") as f:
                seen_ids = [line.strip() for line in f.readlines()]
        with open(GLOBAL_COMIC_LIST, "r") as f:
            mangalist = [line.strip() for line in f.readlines()if line.strip()]
        # print(mangalist)
        chapterlists = []
        for manga in mangalist:
            chapterlists += [get_chapter_id(link) for link in parse_link(manga)]
            time.sleep(GLOBAL_SLEEP)
        # print(chapterlists)
        # print(f"Found {len(chapterlists)} ")
        new_chapters = [id for id in chapterlists if id not in seen_ids]
        logging.info(f"Found {len(new_chapters)} new chapters")
        for new_chapter in new_chapters:
            link = f"https://weebcentral.com/chapters/{new_chapter}"
            downloaded = None
            while downloaded is None:
                try:
                    downloaded = full_download(link, GLOBAL_MANGA_PATH)
                except TimeoutError:
                    downloaded = None
                    logging.info("Timeout in main (will continue)")
            logging.info(f"Downloaded {downloaded['series']} {downloaded['chapter']}")
            send_message(embed_content=f"[{downloaded['series']} - {downloaded['chapter']}]({link})")
            seen_ids.append(new_chapter)
            with open(GLOBAL_SEEN_DATA, "w") as f:
                f.writelines([id+"\n" for id in seen_ids])
            time.sleep(GLOBAL_SLEEP)
        time.sleep(GLOBAL_CHECKER_TIMEOUT)


if __name__ == "__main__":
    main()
