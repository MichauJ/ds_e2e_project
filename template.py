import os
from pathlib import Path   # what for?
import logging

logging.basicConfig(
    level=logging.INFO,
    format= '[%(asctime)s]: %(message)s:'
)

project_name = "ds_e2e_project" # ="datascience"
list_of_files = [
    ".github/workflows/.gitkeep",  # utrzymuje pusty katalog dla konfiguracji GitHub Actions (CI/CD)
    f"src/{project_name}/__init__.py",  # oznacza główny katalog projektu jako pakiet Pythona
    f"src/{project_name}/components/__init__.py",  # pakiet na komponenty (np. moduły logiki biznesowej)
    f"src/{project_name}/utils/__init__.py",  # pakiet z funkcjami pomocniczymi (utilities)
    f"src/{project_name}/utils/common.py",  # wspólne funkcje pomocnicze używane w wielu miejscach
    f"src/{project_name}/config/__init__.py",  # pakiet konfiguracji projektu
    f"src/{project_name}/config/configuration.py",  # logika ładowania i zarządzania konfiguracją
    f"src/{project_name}/pipeline/__init__.py",  # pakiet dla pipeline’ów (przepływów danych)
    f"src/{project_name}/pipeline/ingestion/__init__.py",  # pipeline do pobierania/dostarczania danych
    f"src/{project_name}/pipeline/inference/__init__.py",  # pipeline do inferencji (predykcji)
    f"src/{project_name}/__init__.py",  # (duplikat) inicjalizacja pakietu głównego – można usunąć
    f"src/{project_name}/entity/__init__.py",  # pakiet z definicjami encji (np. struktur danych)
    f"src/{project_name}/entity/config_entity.py",  # klasy reprezentujące konfigurację jako obiekty
    f"src/{project_name}/constants/__init__.py",  # stałe używane w projekcie (np. nazwy plików, ścieżki)
    "config/config.yaml",  # główny plik konfiguracyjny (np. ścieżki, ustawienia pipeline’u)
    "params.yaml",  # parametry eksperymentów/modelu (np. hiperparametry)
    "schema.yaml",  # definicja schematu danych (np. walidacja wejścia)
    "main.py",  # punkt wejścia aplikacji (uruchamianie pipeline’u lub serwera)
    "Dockerfile",  # instrukcja budowania obrazu Dockera dla aplikacji
    "setup.py",  # konfiguracja pakietu (instalacja projektu jako biblioteki)
    "research/research.ipynb",  # notebook do eksperymentów i analizy danych
    "templates/index.html",  # szablon HTML (np. dla prostego interfejsu webowego)
]

# Iteruje po liście ścieżek plików, tworząc brakujące katalogi i pliki
for filepath in list_of_files:
    filepath = Path(filepath)  # zamienia ścieżkę (string) na obiekt Path (łatwiejsza praca ze ścieżkami)

    filedir, filename = os.path.split(filepath)  # rozdziela ścieżkę na katalog i nazwę pliku

    # Jeśli katalog istnieje w ścieżce (nie jest pusty)
    if filedir != "":
        os.makedirs(filedir, exist_ok=True)  # tworzy katalog (i ewentualnie nadrzędne), jeśli nie istnieje
        logging.info(f"Creating directory {filedir} for the file: {filename}")  # loguje utworzenie katalogu

    # Jeśli plik nie istnieje LUB istnieje, ale jest pusty (rozmiar 0)
    if (not os.path.exists(filepath)) or (os.path.getsize(filepath) == 0):
        with open(filepath, "w") as f:  # tworzy nowy pusty plik (lub nadpisuje istniejący pusty)
            pass  # brak operacji – plik ma być tylko utworzony
            logging.info(f"Creating empty file: {filepath}")  # loguje utworzenie pliku
    else:
        # Jeśli plik istnieje i nie jest pusty – nic nie robi
        logging.info(f"{filename} already exists")  # loguje, że plik już istnieje