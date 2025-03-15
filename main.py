import nodriver as uc
from nodriver import *
import asyncio
from dotenv import load_dotenv
from scraper.GenimedesMonitor import GenimedesMonitor, Browsers


async def load_browser(browser_name: str) -> uc.Browser:
    browser = await uc.start(
        headless=False,
        browser_executable_path=f"/snap/bin/{browser_name}",
        user_data_dir="./uc-user-data",
    )
    return browser


async def main() -> None:
    load_dotenv(override=True)

    browser = await load_browser(Browsers.CHROMIUM.value)
    monitor = GenimedesMonitor(browser)
    await monitor.scrape(browser)


if __name__ == "__main__":
    asyncio.run(main())
