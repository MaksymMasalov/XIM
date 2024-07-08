from pdf_utils.reader import extract_pdf_info
from pdf_utils.validator import check_pdf_structure

# Загрузка и парсинг эталонного PDF файла
template_info = extract_pdf_info('test_task.pdf')

# Указание пути к тестируемому PDF файлу
test_pdf_path = 'path_to_test_pdf.pdf'

# Загрузка и парсинг тестируемого PDF файла
test_info = extract_pdf_info(test_pdf_path)

# Проверка соответствия структуры
is_valid_structure = check_pdf_structure(template_info, test_info)
print(f"Does the test PDF have a valid structure? {is_valid_structure}")
