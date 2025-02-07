# Weebcentral Downloader for Kavita
This project is meant to help me with automating my [Kavita](https://www.kavitareader.com/) library by automatically downloading from Weebcentral, therefore removing my need to check for updates in [Hakuneko](https://github.com/manga-download/hakuneko). This might soon be arbitrary as its next Version [Haruneko](https://github.com/manga-download/haruneko) might be able to run and auto-download in the background as well.

## Initial Setup
- rename example.manga.txt to manga.txt and fill it with the links to the series you want to download
- Optionally change download directory in main.py
- Optionally rename example.discord.txt to discord.txt and give it a webhook url to automatically get Discord notfications
- Optionally use [pyinstaller](https://pyinstaller.org/en/stable/) to convert it into a headless .exe file

## Installation
- ```pip install -r requirements.txt```
- ```playwright install``` to install the browser engine needed
- create an environment variable called PLAYWRIGHT_BROWSER_PATH and point it to the folder playwright saved to (default under windows: %localappdata%\ms-playwright)
- Optionally ```pyinstaller --onefile --noconsole main.py```, then copy exe file from dist folder and place it here
- Optionally win+r shell:startup and place a shortcut to the exe there
