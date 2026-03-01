import os
import pandas as pd
from langchain_core.tools import tool

# Путь к CSV‑файлу с требованиями
FILE_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'requirements', 'functional_requirements.csv')


def _ensure_file_exists():
    """Создаёт файл с заголовком, если его ещё нет."""
    if not os.path.exists(FILE_PATH):
        df = pd.DataFrame(columns=['ID', 'Requirement'])
        df.to_csv(FILE_PATH, index=False, header=True, encoding='utf-8')

@tool
def get_all_requirements():
    """Возвращает список всех требований в виде списка словарей."""
    _ensure_file_exists()
    df = pd.read_csv(FILE_PATH, dtype=str)
    return df.to_dict(orient='records')

@tool
def get_requirement_by_id(req_id):
    """Возвращает требование по его ID или None, если не найдено."""
    _ensure_file_exists()
    df = pd.read_csv(FILE_PATH, dtype=str)
    result = df[df['ID'] == str(req_id)]
    return result.iloc[0].to_dict() if not result.empty else None

@tool
def add_requirement(req_id, requirement):
    """Добавляет новое требование. При конфликте ID возбуждает ValueError."""
    _ensure_file_exists()
    df = pd.read_csv(FILE_PATH, dtype=str)
    if req_id in df['ID'].values:
        raise ValueError(f"Requirement with ID {req_id} already exists")
    new_row = pd.DataFrame({'ID': [req_id], 'Requirement': [requirement]})
    df = pd.concat([df, new_row], ignore_index=True)
    df.to_csv(FILE_PATH, index=False, header=True, encoding='utf-8')

@tool()
def update_requirement(req_id, new_requirement):
    """Обновляет требование с заданным ID."""
    _ensure_file_exists()
    df = pd.read_csv(FILE_PATH, dtype=str)
    if req_id not in df['ID'].values:
        raise ValueError(f"Requirement with ID {req_id} not found")
    df.loc[df['ID'] == req_id, 'Requirement'] = new_requirement
    df.to_csv(FILE_PATH, index=False, header=True, encoding='utf-8')

@tool
def delete_requirement(req_id):
    """Удаляет требование с заданным ID."""
    _ensure_file_exists()
    df = pd.read_csv(FILE_PATH, dtype=str)
    if req_id not in df['ID'].values:
        raise ValueError(f"Requirement with ID {req_id} not found")
    # TODO: изменить поведение на изменение атрибута, а не физического удаления
    df = df[df['ID'] != req_id]
    df.to_csv(FILE_PATH, index=False, header=True, encoding='utf-8')