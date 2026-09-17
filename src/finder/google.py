from src.acquisition.models.discovered_file import DiscoveredFile
from bs4 import BeautifulSoup
from bs4 import Tag
from src.finder.playwright_loader import PlaywrightLoader, FindSomething

FILE_EXTENSION = [  ".pdf",
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
                    ".py"
                ]
class Google:

    @staticmethod
    def folder_old(url: str) -> list:
        html = PlaywrightLoader.load(url)
        names = FindSomething.extract_names_from_table(html)
        return [
            DiscoveredFile(name=name, url=url)
            for name in names]


    @staticmethod
    def folder(url: str) -> list:
        html = PlaywrightLoader.load(url)
        soup = BeautifulSoup(html, "html.parser")
        files = []
        seen_names = set()

        for element in soup.find_all():
            if not isinstance(element, Tag):
                continue

            if element.name in ("script", "style", "noscript"):
                continue

            if element.find(True) is not None:
                continue

            text = element.get_text(strip=True)
            try:
                text = text.removesuffix("Compartilhado")
            except:
                pass
            if not text:
                continue

            if not any(
                text.lower().endswith(ext) for ext in FILE_EXTENSION
            ):
                continue

            if text in seen_names:
                continue
            parent = element

            file_id = None

            for _ in range(10):

                parent = parent.parent

                if "data-id" in parent.attrs:
                    file_id = parent["data-id"]

                    break

            seen_names.add(text)

            download_url = (
                f"https://drive.google.com/uc"
                f"?export=download&id={file_id}"
            )

            files.append(
                DiscoveredFile(
                    name=text,
                    url=download_url,
                    file_id=file_id,
                )
            )

        return files

    @staticmethod
    def folder_carregando_1(url: str) -> list:
        html = PlaywrightLoader.load(url)
        soup = BeautifulSoup(html, "html.parser")
        files = []
        seen_names = set()

        for element in soup.find_all():
            # ignora tags que não representam conteúdo visível
            if element.name in ("script", "style", "noscript"):
                continue

            # só considera elementos-folha (sem filhos que sejam tags).
            # isso evita que um <div> "wrapper" que só contém um <strong>
            # com o nome do arquivo seja contado de novo (get_text() em
            # um ancestral repete o mesmo texto do descendente).
            if element.find(True) is not None:
                continue

            text = element.get_text(strip=True)
            if not text:
                continue

            if not any(
                text.lower().endswith(ext) for ext in FILE_EXTENSION
            ):
                continue

            if text in seen_names:
                continue
            seen_names.add(text)

            files.append(
                DiscoveredFile(
                    name=text,
                    url=url,
                )
            )

        return files

    @staticmethod
    def folder_carregando_old(url: str) -> list:
        html = PlaywrightLoader.load(url)
        soup = BeautifulSoup(html,"html.parser")
        files = []
        for element in soup.find_all():
            text = element.get_text(
                strip=True
            )
            if not text:
                continue
            if any(
                text.lower().endswith(ext)
                for ext in FILE_EXTENSION):
                    files.append(
                        DiscoveredFile(
                            name=text,
                            url=url,
                        )
                    )

        return files

    @staticmethod
    def is_drive_file(url: str) -> bool:
        return "drive.google.com/file/d/" in url

    @staticmethod
    def is_drive_folder(url: str) -> bool:
        return "drive.google.com/drive/folders/" in url

    @staticmethod
    def extract_file_id(url: str) -> str:
        return url.split("/file/d/")[1].split("/")[0]

    @staticmethod
    def extract_folder_id(url: str) -> str:
        return url.split("/folders/")[1].split("?")[0]

    @staticmethod
    def build_download_url(file_id: str) -> str:
        return (
            f"https://drive.google.com/uc"
            f"?export=download&id={file_id}"
        )



