import requests
import os
import re
import shutil
import tkinter as tk
from tkinter import filedialog

def select_directory(title="Selecione o diretório"):
    root = tk.Tk()
    root.withdraw()
    directory = filedialog.askdirectory(title=title)
    return directory

def main():
    ads_directory = select_directory("Selecione o diretório onde está localizado o Black Desert (ex: C:\\BlackDesert)")
    if not ads_directory:
        print("Diretório do Black Desert não selecionado. Saindo...")
        return

    ads_url = "http://naeu-o-dn.playblackdesert.com/UploadData/ads_files"
    response = requests.get(ads_url)
    content = response.text

    match = re.search(r'languagedata_en\.loc\s+(\d+)', content)
    if match:
        version_number = match.group(1)
        print(f"Versão encontrada: {version_number}")
    else:
        print("Versão não encontrada.")
        return

    loc_url = f"http://naeu-o-dn.playblackdesert.com/UploadData/ads/languagedata_en/{version_number}/languagedata_en.loc"

    download_response = requests.get(loc_url)
    download_directory = os.path.join(os.environ['USERPROFILE'], 'Downloads', 'languagedata_en.loc')
    with open(download_directory, 'wb') as f:
        f.write(download_response.content)
    
    ads_directory = os.path.join(ads_directory, 'ads')

    for filename in os.listdir(ads_directory):
        old_file = os.path.join(ads_directory, filename)
        new_file = os.path.join(ads_directory, f"backup_{filename}")
        os.rename(old_file, new_file)

    move_downloaded_file = os.path.join(ads_directory, 'languagedata_pt.loc')
    shutil.move(download_directory, move_downloaded_file)

if __name__ == "__main__":
    main()
