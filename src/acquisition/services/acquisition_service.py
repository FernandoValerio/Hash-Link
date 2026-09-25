from pathlib import Path

from src.acquisition.validators import validate_url, detect_source_type
from src.acquisition.models import AcquisitionResult, DiscoveredFile
from src.finder import Google, Microsoft
from src.finder.playwright_loader import LoginDetector, AuthenticationManager, resolve_profile, SessionManager


class AcquisitionService:
    def analyse(self, source):
        """Ponto de entrada único: reconhece sozinho se `source` é uma URL,
        um arquivo local ou uma pasta local, e direciona para a análise
        correspondente."""
        source = (source or "").strip()
        source_type = detect_source_type(source)

        if source_type == "local_file":
            result = self._analyse_local_file(source)
            print(result)
            return result
        if source_type == "local_folder":
            return self._analyse_local_folder(source)
        if source_type == "url":
            return self._analyse_url(source)

        raise ValueError(
            "Origem inválida: informe uma URL (http/https) ou um caminho local "
            "existente (arquivo ou pasta)."
        )

    def _analyse_local_file(self, path_str: str) -> AcquisitionResult:
        path = Path(path_str.strip('"').strip("'"))
        discovered = [
            DiscoveredFile(
                name=path.name,
                is_local=True,
                local_path=str(path.resolve()),
                size=path.stat().st_size,
            )
        ]
        return AcquisitionResult(str(path), str(path), 200, "local/file", discovered_files=discovered)

    def _analyse_local_folder(self, path_str: str) -> AcquisitionResult:
        root = Path(path_str.strip('"').strip("'"))
        discovered = [
            DiscoveredFile(
                name=str(file_path.relative_to(root)),
                is_local=True,
                local_path=str(file_path.resolve()),
                size=file_path.stat().st_size,
            )
            for file_path in sorted(root.rglob("*"))
            if file_path.is_file()
        ]
        return AcquisitionResult(str(root), str(root), 200, "local/folder", discovered_files=discovered)

    def _analyse_url(self, url):
        if not validate_url(url): raise ValueError("Invalid URL")
        #no caso de drive extrair o file ID
        discovered_files = []
        profile = resolve_profile(url)
        if profile and not SessionManager.has_valid_session(profile):
            SessionManager.login_interactive(url, profile)
        # if LoginDetector.requires_login(url):
        #     AuthenticationManager.authenticate(url, profile=resolve_profile(url) or "default")

        if "drive.google.com/file/d/" in url:
            file_id = url.split("/file/d/")[1].split("/")[0]
            download_url = (
             f"https://drive.google.com/uc"
             f"?export=download&id={file_id}"
            )
            discovered_files.append(
                DiscoveredFile(
                    name=f"google_drive_{file_id}",
                    url=download_url,
                )
            )
        if "drive.google.com/drive/folders/" in url:
            folder_id = (
                url.split("/folders/")[1]
                .split("?")[0]
            )
            discovered_files = Google.folder(url)
        if Microsoft.is_onedrive_folder(url):
            discovered_files = Microsoft.folder(url)
            print(discovered_files)


        return AcquisitionResult(url,url,200,"text/html",discovered_files=discovered_files)