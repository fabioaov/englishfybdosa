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

def on_language_select(language, root):
    global selected_language
    selected_language = language
    root.destroy()

def main():
    global selected_language
    selected_language = None
    root = tk.Tk()
    root.title("Seleção de Linguagem")
    
    pt_button = tk.Button(root, text="PT", command=lambda: on_language_select("PT", root))
    pt_button.pack(pady=10)
    
    es_button = tk.Button(root, text="ES", command=lambda: on_language_select("ES", root))
    es_button.pack(pady=10)
    
    root.mainloop()
    
    if selected_language is None:
        print("Nenhuma linguagem selecionada. Abortando...")
        return
    
    ads_directory = select_directory("Selecione o diretório onde está localizado o Black Desert (ex: C:\\BlackDesert)")
    if not ads_directory:
        return
    
    ads_directory_path = os.path.join(ads_directory, 'ads')
    if not os.path.exists(ads_directory_path):
        print("Diretório inválido. Abortando...")
        return
    
    ads_url = "http://naeu-o-dn.playblackdesert.com/UploadData/ads_files"
    response = requests.get(ads_url)
    content = response.text

    match = re.search(r'languagedata_en\.loc\s+(\d+)', content)
    if match:
        version_number = match.group(1)
    else:
        return

    loc_url = f"http://naeu-o-dn.playblackdesert.com/UploadData/ads/languagedata_en/{version_number}/languagedata_en.loc"
    download_response = requests.get(loc_url)
    download_directory = os.path.join(os.environ['USERPROFILE'], 'Downloads', 'languagedata_en.loc')
    with open(download_directory, 'wb') as f:
        f.write(download_response.content)

    language_map = {
        "PT": "languagedata_pt.loc",
        "ES": "languagedata_es.loc"
    }

    target_filename = language_map[selected_language]
    has_backup = any(filename.startswith("backup_") for filename in os.listdir(ads_directory_path))

    if not has_backup:
        for filename in os.listdir(ads_directory_path):
            if filename == target_filename:
                old_file = os.path.join(ads_directory_path, filename)
                new_file = os.path.join(ads_directory_path, f"backup_{filename}")
                os.rename(old_file, new_file)

    target_file = os.path.join(ads_directory_path, target_filename)
    if os.path.exists(target_file):
        backup_target_file = os.path.join(ads_directory_path, f"backup_{os.path.basename(target_file)}")
        if not os.path.exists(backup_target_file):
            os.rename(target_file, backup_target_file)
        else:
            os.remove(target_file)

    shutil.move(download_directory, target_file)

if __name__ == "__main__":
    main()
