from playwright.sync_api import sync_playwright
from pathlib import Path
import subprocess
import sys

from bs4 import BeautifulSoup


COLUMN_NAMES = {
    "nome",
    "name",
    "arquivo",
    "file",
    "filename",
}


SESSION_FILE = (
    Path("resources")
    / "session.json"
)

DOMAIN_PROFILES = {
    "onedrive.live.com": "microsoft",
    "1drv.ms": "microsoft",
    "sharepoint.com": "microsoft",
    "drive.google.com": "google",
    "docs.google.com": "google",
}


def resolve_profile(url: str) -> str | None:
    for domain, profile in DOMAIN_PROFILES.items():
        if domain in url:
            return profile
    return None

class SessionManager:
    SESSION_DIR = Path("resources/sessions")

    @classmethod
    def get_session_file(cls, profile: str) -> Path:
        cls.SESSION_DIR.mkdir(parents=True, exist_ok=True)
        return cls.SESSION_DIR / f"{profile}.json"

    @classmethod
    def has_valid_session(cls, profile: str) -> bool:
        return cls.get_session_file(profile).exists()

    @classmethod
    def login_interactive(cls, url: str, profile: str):
        session_file = cls.get_session_file(profile)
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=False)
            context = browser.new_context()
            page = context.new_page()
            page.goto(url, wait_until="domcontentloaded")
            print("\nFaça login e conclua o MFA.")
            print("Depois pressione ENTER.\n")
            input()
            context.storage_state(path=str(session_file))
            browser.close()

    @classmethod
    def get_context(cls, profile: str, headless: bool = True):
        p = sync_playwright().start()
        browser = p.chromium.launch(headless=headless)
        session_file = cls.get_session_file(profile)
        if session_file.exists():
            return browser.new_context(storage_state=str(session_file))
        return browser.new_context()


class PlaywrightLoader:

    @staticmethod
    def ensure_playwright():

        try:

            from playwright.sync_api import (
                sync_playwright
            )

            with sync_playwright() as p:

                browser = p.chromium.launch()

                browser.close()

            return True

        except Exception:

            subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "playwright",
                    "install",
                    "chromium",
                ],
                check=True
            )

            return True

    @staticmethod
    def load(url: str, profile: str | None = None) -> str:
        PlaywrightLoader.ensure_playwright()

        profile = profile or resolve_profile(url)

        if profile:
            context = SessionManager.get_context(profile=profile, headless=True)
            page = context.new_page()
            try:
                page.goto(url, wait_until="networkidle", timeout=60000)
                html = page.content()
            finally:
                context.close()
            return html

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto(url, wait_until="networkidle", timeout=60000)
            html = page.content()
            browser.close()
            return html

class AuthenticationManager:

    PROFILE_DIR = (
        Path("resources")
        / "profiles"
    )

    playwright = None
    context = None
    page = None

    @classmethod
    def get_profile_path(
        cls,
        profile: str = "microsoft"
    ) -> Path:

        cls.PROFILE_DIR.mkdir(
            parents=True,
            exist_ok=True
        )

        return (
            cls.PROFILE_DIR
            / profile
        )

    @classmethod
    def authenticate(
        cls,
        url: str,
        profile: str = "microsoft"
    ):

        profile_path = cls.get_profile_path(
            profile
        )

        cls.playwright = (
            sync_playwright()
            .start()
        )

        cls.context = (
            cls.playwright.chromium
            .launch_persistent_context(
                user_data_dir=str(
                    profile_path
                ),
                headless=False,
            )
        )

        pages = cls.context.pages

        if pages:
            cls.page = pages[0]
        else:
            cls.page = cls.context.new_page()

        cls.page.goto(url)

        print(
            "\n================================="
        )

        print(
            "Faça login."
        )

        print(
            "Conclua o MFA."
        )

        print(
            "Abra a pasta desejada."
        )

        print(
            "Depois pressione ENTER."
        )

        print(
            "=================================\n"
        )

        input()

        cls.context.close()
        cls.playwright.stop()

        print(
            "\nSessão armazenada."
        )

        print(
            cls.page.url
        )

    @classmethod
    def get_context(
        cls,
        profile: str = "microsoft",
        headless: bool = True,
    ):

        profile_path = cls.get_profile_path(
            profile
        )

        p = sync_playwright().start()

        context = (
            p.chromium
            .launch_persistent_context(
                user_data_dir=str(
                    profile_path
                ),
                headless=headless,
            )
        )

        return context

    @classmethod
    def clear_profile(
        cls,
        profile: str = "microsoft"
    ):

        import shutil

        profile_path = cls.get_profile_path(
            profile
        )

        if profile_path.exists():

            shutil.rmtree(
                profile_path
            )

            print(
                f"Perfil removido: {profile}"
            )


class AuthenticationManager_v2:
    SESSION_DIR = Path(
        "resources/sessions"
    )

    @classmethod
    def get_session_file(
            cls,
            profile: str = "default"
    ) -> Path:
        cls.SESSION_DIR.mkdir(
            parents=True,
            exist_ok=True
        )

        return (
                cls.SESSION_DIR
                / f"{profile}.json"
        )

    @classmethod
    def authenticate(
            cls,
            url: str,
            profile: str = "microsoft"
    ) -> bool:
        session_file = cls.get_session_file(
            profile
        )

        with sync_playwright() as p:
            browser = p.chromium.launch(
                headless=False
            )

            context = browser.new_context()

            page = context.new_page()

            page.goto(
                url,
                wait_until="domcontentloaded"
            )

            print(
                "\n================================="
            )
            print(
                "Conclua o login e o MFA."
            )
            print(
                "Depois navegue até a pasta"
            )
            print(
                "que deseja acessar."
            )
            print(
                "Somente então pressione ENTER."
            )
            print(
                "=================================\n"
            )

            input()

            print(
                "\nURL após login:"
            )

            print(page.url)

            context.storage_state(
                path=str(session_file)
            )


class AuthenticationManager_old:

    @staticmethod
    def authenticate(url: str) -> bool:
        """
        Abre um navegador real para o usuário
        realizar autenticação.
        """

        SESSION_FILE.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        with sync_playwright() as p:

            browser = p.chromium.launch(
                headless=False
            )

            context = browser.new_context()

            page = context.new_page()

            page.goto(url)

            print(
                "\nRealize o login no navegador."
            )

            input(
                "\nApós concluir o login "
                "pressione ENTER..."
            )

            context.storage_state(
                path=str(SESSION_FILE)
            )

            browser.close()

        return True

    @staticmethod
    def has_session() -> bool:
        """
        Verifica se existe sessão salva.
        """

        return SESSION_FILE.exists()

    @staticmethod
    def create_authenticated_context(
        playwright,
    ):
        """
        Cria contexto reutilizando a sessão.
        """

        if SESSION_FILE.exists():

            return playwright.chromium.launch(
                headless=True
            ).new_context(
                storage_state=str(
                    SESSION_FILE
                )
            )

        return playwright.chromium.launch(
            headless=True
        ).new_context()

    @staticmethod
    def clear_session():
        """
        Remove sessão salva.
        """

        if SESSION_FILE.exists():

            SESSION_FILE.unlink()

    @staticmethod
    def get_storage_path() -> str:

        return str(
            SESSION_FILE
        )

class LoginDetector:

    @staticmethod
    def requires_login(url: str) -> bool:

        with sync_playwright() as p:

            browser = p.chromium.launch(
                headless=True
            )

            page = browser.new_page()

            page.goto(
                url,
                wait_until="domcontentloaded"
            )

            page.wait_for_timeout(5000)

            #
            # 1. Procura campos de senha
            #
            if page.locator(
                'input[type="password"]'
            ).count() > 0:

                browser.close()
                return True

            #
            # 2. Procura campos de email
            #
            if page.locator(
                'input[type="email"]'
            ).count() > 0:

                browser.close()
                return True

            #
            # 3. Procura formulários de login
            #
            if page.locator(
                'form'
            ).count() > 0:

                title = page.title().lower()

                if any(
                    word in title
                    for word in (
                        "login",
                        "sign in",
                        "entrar",
                        "acessar",
                    )
                ):
                    browser.close()
                    return True

            #
            # 4. Verifica URL final
            #
            final_url = page.url.lower()

            login_keywords = (
                "login",
                "signin",
                "sign-in",
                "oauth",
                "authorize",
                "auth",
                "saml",
            )

            if any(
                keyword in final_url
                for keyword in login_keywords
            ):
                browser.close()
                return True

            browser.close()

            return False


class PlaywrightLoader_old:

    @staticmethod
    def load(url: str, profile: str | None = None) -> str:

        profile = profile or resolve_profile(url)

        if profile:
            context = AuthenticationManager.get_context(
                profile=profile,
                headless=True
            )
            page = context.new_page()
            try:
                page.goto(url, wait_until="networkidle", timeout=60000)
                html = page.content()
            finally:
                context.close()
            return html

        # sem perfil conhecido: mantém o comportamento antigo
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto(url, wait_until="networkidle", timeout=60000)
            html = page.content()
            browser.close()
            return html

    @staticmethod
    def load_old(url: str) -> str:

        with sync_playwright() as p:

            browser = p.chromium.launch(
                headless=True
            )

            page = browser.new_page()

            page.goto(
                url,
                wait_until="networkidle",
                timeout=60000,
            )
            # page.goto(url)
            #
            # page.wait_for_timeout(5000)
            #
            # print(page.frames)

            html = page.content()

            browser.close()

            return html

class FindSomething:

    @staticmethod
    def extract_names_from_table(html: str) -> list:
        soup = BeautifulSoup(html, "html.parser")

        results = []

        #
        # procura tabelas HTML
        #
        for table in soup.find_all("table"):

            headers = []

            header_row = table.find("tr")

            if not header_row:
                continue

            for th in header_row.find_all(["th", "td"]):
                headers.append(
                    th.get_text(strip=True).lower()
                )

            target_index = None

            for index, header in enumerate(headers):

                if header in COLUMN_NAMES:
                    target_index = index
                    break

            if target_index is None:
                continue

            rows = table.find_all("tr")[1:]

            for row in rows:

                cols = row.find_all(["td", "th"])

                if len(cols) <= target_index:
                    continue

                value = cols[target_index].get_text(
                    strip=True
                )

                if value:
                    results.append(value)

        return results
