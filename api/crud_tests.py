import os
import pandas as pd

# Путь к CSV‑файлу с тестами
FILE_PATH = os.path.join(os.path.dirname(__file__), '..', 'tests', 'test_checklist.csv')


def _ensure_file_exists():
    """Создаёт файл с заголовком, если его ещё нет."""
    if not os.path.exists(FILE_PATH):
        df = pd.DataFrame(columns=['ID', 'Title', 'Description'])
        df.to_csv(FILE_PATH, index=False, header=True, encoding='utf-8')


def get_all_tests():
    """Возвращает список всех тестов в виде списка словарей."""
    _ensure_file_exists()
    df = pd.read_csv(FILE_PATH, dtype=str)
    return df.to_dict(orient='records')


def get_test_by_id(test_id):
    """Возвращает тест по его ID или None, если не найден."""
    _ensure_file_exists()
    df = pd.read_csv(FILE_PATH, dtype=str)
    result = df[df['ID'] == str(test_id)]
    return result.iloc[0].to_dict() if not result.empty else None


def add_test(test_id, title, description):
    """Добавляет новый тест. При конфликте ID возбуждает ValueError."""
    _ensure_file_exists()
    df = pd.read_csv(FILE_PATH, dtype=str)
    if test_id in df['ID'].values:
        raise ValueError(f"Test with ID {test_id} already exists")
    new_row = pd.DataFrame({'ID': [test_id], 'Title': [title], 'Description': [description]})
    df = pd.concat([df, new_row], ignore_index=True)
    df.to_csv(FILE_PATH, index=False, header=True, encoding='utf-8')


def update_test(test_id, new_title, new_description):
    """Обновляет тест с заданным ID."""
    _ensure_file_exists()
    df = pd.read_csv(FILE_PATH, dtype=str)
    if test_id not in df['ID'].values:
        raise ValueError(f"Test with ID {test_id} not found")
    df.loc[df['ID'] == test_id, ['Title', 'Description']] = new_title, new_description
    df.to_csv(FILE_PATH, index=False, header=True, encoding='utf-8')


def delete_test(test_id):
    """Удаляет тест с заданным ID."""
    _ensure_file_exists()
    df = pd.read_csv(FILE_PATH, dtype=str)
    if test_id not in df['ID'].values:
        raise ValueError(f"Test with ID {test_id} not found")
    df = df[df['ID'] != test_id]
    df.to_csv(FILE_PATH, index=False, header=True, encoding='utf-8')