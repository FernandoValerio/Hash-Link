from src.acquisition.validators import validate_url
from src.acquisition.models import AcquisitionResult, DiscoveredFile
from src.finder import Google, Microsoft
from src.finder.playwright_loader import LoginDetector, AuthenticationManager, resolve_profile, SessionManager


class AcquisitionService:
    def analyse(self,url):
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
