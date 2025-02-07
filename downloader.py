import os

import requests
from bs4 import BeautifulSoup, Tag
from cbz.comic import ComicInfo
from cbz.constants import PageType
from cbz.page import PageInfo
from playwright.sync_api import sync_playwright


def get_metadata(htmlcontent: str) -> dict[str, str]:
    parser = BeautifulSoup(htmlcontent, "html.parser")
    # title = parser.find("title")
    # if title is None:
    #     raise Exception("Parsing Error in getting title")
    # if not isinstance(title, Tag):
    #     raise Exception("Parsing Error with title tag")
    # print(f"Title: {title.get_text()}")
    seriesnamecontainer = parser.find(
        "div", class_="w-full flex items-center justify-center gap-2 p-4"
    )
    if not isinstance(seriesnamecontainer, Tag):
        raise Exception("SeriesNameTag")
    seriesnamespan = seriesnamecontainer.findChild("span", class_="truncate")
    if not isinstance(seriesnamespan, Tag):
        raise Exception("SeriesNameSpan")
    seriesname = seriesnamespan.get_text()

    chapternamecontainer = parser.find(
        "button", class_="col-span-4 lg:flex-1 btn btn-secondary"
    )
    if not isinstance(chapternamecontainer, Tag):
        print(type(chapternamecontainer))
        raise Exception("ChapterNameTag")
    chapternamespan = chapternamecontainer.findChild("span")
    if not isinstance(chapternamespan, Tag):
        raise Exception("ChapterNameSpan")
    chaptername = chapternamespan.get_text()

    return {"series": seriesname, "chapter": chaptername}




def get_image_links_playwright(link: str) -> list[str]:
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(link, timeout=10000)
        page.wait_for_selector(
            'main section img[alt*="Page"]:not([x-show])', timeout=10000
        )
        image_urls = page.eval_on_selector_all(
            'main section img[alt*="Page"]:not([x-show])',
            "elements => elements.map(img=>img.src)",
        )
        if len(image_urls) == 0 or len(image_urls[0]) == 0:
            raise Exception("EmptyImageUrls")
        return image_urls


def download_chapter_to_cbz(
    chaptername: str, seriesname: str, image_links: list[str], store_path: str
):
    imagedata = []
    for image_link in image_links:
        rq = requests.get(image_link)
        if rq.status_code != 200:
            raise Exception(f"Failed to download image {image_link}")
        imagedata.append(rq.content)
    pages = [PageInfo.loads(data, type=PageType.STORY) for data in imagedata]
    comic = ComicInfo.from_pages(pages=pages, title=chaptername, series=seriesname)
    folder = os.path.join(store_path, seriesname)
    if not os.path.exists(folder):
        os.mkdir(folder)
    cbzcontent = comic.pack()
    filepath = os.path.join(folder, f"{chaptername}.cbz")
    with open(filepath, "wb") as outfile:
        outfile.write(cbzcontent)
    # print(f"Downloaded {seriesname} : {chaptername} with {len(pages)} pages")


def full_download(link: str, store_path: str = "download"):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:135.0) Gecko/20100101 Firefox/135.0"
    }
    rq = requests.get(link, headers=headers)
    if rq.status_code != 200:
        raise Exception(f"Status Code {rq.status_code} at {link}")
    # with open("debug2.html", "w") as f:
    #     f.write(rq.text)
    # print(f"FULL DOWNLOAD {link}")
    metadata = get_metadata(rq.text)
    # print(metadata)
    imagelinks = get_image_links_playwright(link)
    download_chapter_to_cbz(
        metadata["chapter"], metadata["series"], imagelinks, store_path
    )
    return metadata
    # [print(i) for i in imagelinks]


if __name__ == "__main__":
    full_download("https://weebcentral.com/chapters/01J76XYZY082SV13G02H90QZB1")
