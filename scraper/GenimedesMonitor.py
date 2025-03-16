import nodriver as uc
from nodriver import *
import os
from enum import Enum


class Browsers(Enum):
    CHROMIUM = "chromium"
    # FIREFOX = "firefox"
    # EDGE = "edge"


class GenimedesMonitor:
    def __init__(self, browser: uc.Browser):
        self.main_url = "https://www2.ime.usp.br/ganimedes/public/login.xhtml"
        self.browser = browser
        self.credentials = {"user": os.getenv("USER"), "password": os.getenv("PASS")}

    async def _login(self, page: uc.Tab) -> None:
        user, password = self.credentials.get("user"), self.credentials.get("password")
        if not user or not password:
            raise Exception("User or password not found in .env")

        user_input = await page.find("#loginUsuario")
        await user_input.send_keys(user)

        password_input = await page.find("#senhaUsuario")
        await password_input.send_keys(password)

        login_btn = await page.find("#botaoLogin")
        await login_btn.mouse_click()

        # TODO:
        err = await page.find("Internal Server Error")
        if err:
            self.browser.stop()
            raise Exception("Internal Server Error")
        await page.wait(t=2)

    async def _get_login_form(self, page: uc.Tab) -> None:
        get_login_form_btn = await page.find(text="Entrar com Senha única USP")
        await page.wait()
        await get_login_form_btn.mouse_click()

    async def scrape(self, browser: uc.Browser) -> None:
        page = await browser.get(self.main_url)

        await self._get_login_form(page)
        await self._login(page)
