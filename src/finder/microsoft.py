from src.acquisition.models.discovered_file import DiscoveredFile
from bs4 import BeautifulSoup
from bs4 import Tag

from src.finder.playwright_loader import PlaywrightLoader


FILE_EXTENSION = [
    ".pdf",
    ".jpg",
    ".jpeg",
    ".png",
    ".xlsx",
    ".csv",
    ".docx",
    ".zip",
    ".rar",
    ".7z",
    ".mp4",
    ".py",
]


class Microsoft:

    @staticmethod
    def is_onedrive_folder(url: str) -> bool:

        return (
            "onedrive.live.com" in url
            or "1drv.ms" in url
            or "sharepoint.com" in url
        )

    @staticmethod
    def folder(url: str) -> list:

        html = PlaywrightLoader.load(url)

        with open(
                "onedrive_debug.html",
                "w",
                encoding="utf-8"
        ) as f:
            f.write(html)

        print(len(html))

        print(
            html.find("heroField")
        )

        print(
            html.find("role=\"row\"")
        )

        soup = BeautifulSoup(html, "html.parser")

        files = []

        seen = set()

        rows = soup.find_all(
            attrs={"role": "row"}
        )

        for row in rows:

            span = row.find(
                "span",
                attrs={"data-id": "heroField"}
            )

            if span is None:
                continue

            file_name = (
                    span.get("title")
                    or span.get_text(strip=True)
            )

            if not file_name:
                continue

            if file_name in seen:
                continue

            seen.add(file_name)

            files.append(
                DiscoveredFile(
                    name=file_name,
                    url=url,
                )
            )

        return files

