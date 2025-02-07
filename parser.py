import requests
from bs4 import BeautifulSoup


def parse_link(link: str):
    # rq = requests.get(link)
    reallink = get_complete_link(link)
    rq = requests.get(reallink)
    # if rq.status_code != 200:
    #     raise Exception(f"Internal link not found {reallink}")
    # with open("debug.html", "w") as f:
    #     f.write(rq.text)
    parser = BeautifulSoup(rq.text, "html.parser")

    chapterlinks = parser.find_all("a", class_="hover:bg-base-300 flex-1 flex items-center p-2")
    # print(f"{len(chapterlinks)} links found")
    # for chapterlink in chapterlinks:
    #     print(chapterlink["href"])

    
    return [chapterlink["href"] for chapterlink in chapterlinks]


def get_complete_link(link: str) -> str:
    # Convert
    # https://weebcentral.com/series/01J76XYDBHTQFGYQX6G69SJPEW/Blue-Period
    # to
    # https://weebcentral.com/series/01J76XYDBHTQFGYQX6G69SJPEW/full-chapter-list
    if link.endswith("full-chapter-list"):
        return link
    if not link.startswith("https://weebcentral.com/series/"):
        raise Exception(f"Error with link: {link}")
    identifier = link[31:].split("/")
    if len(identifier) > 2:
        raise Exception(f"Error with link: {link}")
    return f"https://weebcentral.com/series/{identifier[0]}/full-chapter-list"



if __name__ == "__main__":
    print(
        parse_link(
            "https://weebcentral.com/series/01J76XY7E827QQQT0ERKCGH4CD/Naruto"
        )
    )
