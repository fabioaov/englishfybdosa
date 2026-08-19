import os
import re
import tkinter as tk
from tkinter import filedialog, messagebox

import requests

ADS_FILES_URL = "http://naeu-o-dn.playblackdesert.com/UploadData/ads_files"
LOC_URL_TEMPLATE = (
    "http://naeu-o-dn.playblackdesert.com/UploadData/ads/languagedata_en/{version}/languagedata_en.loc"
)
REQUEST_TIMEOUT = 60
DOWNLOAD_CHUNK_SIZE = 1 << 20

LANGUAGE_MAP = {
    "PT": "languagedata_pt.loc",
    "ES": "languagedata_es.loc",
}


def select_directory(title="Selecione o diretório"):
    root = tk.Tk()
    root.withdraw()
    directory = filedialog.askdirectory(title=title)
    root.destroy()
    return directory


def select_action():
    selected = {"value": None}
    root = tk.Tk()
    root.title("Englishfy BDO SA")
    root.resizable(False, False)

    def choose(action):
        selected["value"] = action
        root.destroy()

    label = tk.Label(root, text="Escolha uma opção:", font=("Arial", 11, "bold"), padx=20, pady=10)
    label.pack()

    btn_apply = tk.Button(
        root,
        text="Aplicar Inglês",
        width=25,
        height=2,
        command=lambda: choose("apply"),
    )
    btn_apply.pack(padx=20, pady=5)

    btn_restore = tk.Button(
        root,
        text="Restaurar Idioma Original",
        width=25,
        height=2,
        command=lambda: choose("restore"),
    )
    btn_restore.pack(padx=20, pady=5)

    btn_exit = tk.Button(
        root,
        text="Sair",
        width=25,
        height=1,
        command=lambda: choose(None),
    )
    btn_exit.pack(padx=20, pady=(5, 15))

    root.mainloop()
    return selected["value"]


def select_language():
    selected = {"value": None}
    root = tk.Tk()
    root.title("Seleção de Idioma")
    root.resizable(False, False)

    def choose(language):
        selected["value"] = language
        root.destroy()

    label = tk.Label(root, text="Selecione o idioma original do seu jogo:", padx=20, pady=10)
    label.pack()

    for code in LANGUAGE_MAP:
        tk.Button(
            root,
            text=code,
            width=15,
            height=2,
            command=lambda c=code: choose(c),
        ).pack(padx=20, pady=5)

    root.mainloop()
    return selected["value"]


def select_backup_to_restore(available_languages):
    if len(available_languages) == 1:
        return available_languages

    selected = {"value": None}
    root = tk.Tk()
    root.title("Restaurar Idioma")
    root.resizable(False, False)

    def choose(choice):
        selected["value"] = choice
        root.destroy()

    label = tk.Label(root, text="Múltiplos backups encontrados. Qual deseja restaurar?", padx=20, pady=10)
    label.pack()

    for lang in available_languages:
        tk.Button(
            root,
            text=f"Restaurar {lang}",
            width=25,
            height=2,
            command=lambda l=lang: choose([l]),
        ).pack(padx=20, pady=5)

    tk.Button(
        root,
        text="Restaurar Todos",
        width=25,
        height=2,
        command=lambda: choose(available_languages),
    ).pack(padx=20, pady=(5, 15))

    root.mainloop()
    return selected["value"]


def fetch_latest_en_version():
    response = requests.get(ADS_FILES_URL, timeout=REQUEST_TIMEOUT)
    response.raise_for_status()
    match = re.search(r"languagedata_en\.loc\s+(\d+)", response.text)
    if not match:
        raise RuntimeError(
            "Não foi possível localizar a versão de languagedata_en.loc na listagem. "
            f"Conteúdo recebido:\n{response.text!r}"
        )
    return match.group(1)


def download_en_loc(version, destination):
    url = LOC_URL_TEMPLATE.format(version=version)
    with requests.get(url, stream=True, timeout=REQUEST_TIMEOUT) as response:
        response.raise_for_status()
        with open(destination, "wb") as f:
            for chunk in response.iter_content(chunk_size=DOWNLOAD_CHUNK_SIZE):
                f.write(chunk)


def backup_original(target_file):
    if not os.path.exists(target_file):
        return
    backup_file = os.path.join(
        os.path.dirname(target_file), f"backup_{os.path.basename(target_file)}"
    )
    if os.path.exists(backup_file):
        os.remove(target_file)
    else:
        os.rename(target_file, backup_file)


def detect_backups(ads_directory):
    backups = {}
    for code, filename in LANGUAGE_MAP.items():
        backup_path = os.path.join(ads_directory, f"backup_{filename}")
        if os.path.exists(backup_path):
            backups[code] = backup_path
    return backups


def restore_backup(backup_file, target_file):
    os.replace(backup_file, target_file)


def apply_english_flow():
    language = select_language()
    if language is None:
        return

    base_directory = select_directory(
        "Selecione o diretório onde está o Black Desert (ex: C:\\BlackDesert)"
    )
    if not base_directory:
        return

    ads_directory = os.path.join(base_directory, "ads")
    if not os.path.isdir(ads_directory):
        root = tk.Tk()
        root.withdraw()
        messagebox.showerror(
            "Erro",
            f"Pasta 'ads' não encontrada em '{base_directory}'.\n"
            "Selecione a pasta raiz do Black Desert (ex: C:\\BlackDesert).",
        )
        root.destroy()
        return

    target_file = os.path.join(ads_directory, LANGUAGE_MAP[language])
    temp_file = target_file + ".tmp"

    try:
        version = fetch_latest_en_version()
        print(f"Baixando languagedata_en.loc (versão {version})...")
        download_en_loc(version, temp_file)
        backup_original(target_file)
        os.replace(temp_file, target_file)
        print(f"Pronto! '{LANGUAGE_MAP[language]}' agora usa o idioma inglês (versão {version}).")

        root = tk.Tk()
        root.withdraw()
        messagebox.showinfo(
            "Sucesso",
            f"Idioma inglês aplicado com sucesso!\n'{LANGUAGE_MAP[language]}' atualizado para a versão {version}.",
        )
        root.destroy()
    except Exception as exc:
        if os.path.exists(temp_file):
            os.remove(temp_file)
        root = tk.Tk()
        root.withdraw()
        messagebox.showerror("Erro", f"Ocorreu um erro ao aplicar o idioma inglês:\n{exc}")
        root.destroy()


def restore_flow():
    base_directory = select_directory(
        "Selecione o diretório onde está o Black Desert (ex: C:\\BlackDesert)"
    )
    if not base_directory:
        return

    ads_directory = os.path.join(base_directory, "ads")
    if not os.path.isdir(ads_directory):
        root = tk.Tk()
        root.withdraw()
        messagebox.showerror(
            "Erro",
            f"Pasta 'ads' não encontrada em '{base_directory}'.\n"
            "Selecione a pasta raiz do Black Desert (ex: C:\\BlackDesert).",
        )
        root.destroy()
        return

    backups = detect_backups(ads_directory)
    if not backups:
        root = tk.Tk()
        root.withdraw()
        messagebox.showwarning(
            "Aviso",
            f"Nenhum arquivo de backup original encontrado na pasta '{ads_directory}'.",
        )
        root.destroy()
        return

    languages_to_restore = select_backup_to_restore(list(backups.keys()))
    if not languages_to_restore:
        return

    restored = []
    for lang in languages_to_restore:
        backup_path = backups[lang]
        target_path = os.path.join(ads_directory, LANGUAGE_MAP[lang])
        restore_backup(backup_path, target_path)
        restored.append(LANGUAGE_MAP[lang])

    msg = "Arquivos restaurados com sucesso:\n" + "\n".join(restored)
    print(msg)
    root = tk.Tk()
    root.withdraw()
    messagebox.showinfo("Sucesso", msg)
    root.destroy()


def main():
    action = select_action()
    if action == "apply":
        apply_english_flow()
    elif action == "restore":
        restore_flow()


if __name__ == "__main__":
    main()
