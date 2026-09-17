
from src.finder.playwright_loader import PlaywrightLoader

url = "https://governosp-my.sharepoint.com/:f:/r/personal/fernando_flov_policiacientifica_sp_gov_br/Documents/22-P01246?d=wdbc2a84c117e4649bf0153e79834bda0&csf=1&web=1&e=HjEQ8g"

html = PlaywrightLoader.load(url)

print("len:", len(html))
print("heroField:", html.find("heroField"))
print('role="row":', html.find('role="row"'))