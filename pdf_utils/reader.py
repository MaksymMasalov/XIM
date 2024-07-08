from PyPDF2 import PdfReader


def extract_pdf_info(file_path):
    with open(file_path, 'rb') as file:
        # Создаем объект для работы с PDF
        pdf_reader = PdfReader(file)

        # Проверяем, что файл открыт успешно
        if pdf_reader.is_encrypted:
            try:
                pdf_reader.decrypt('')
            except NotImplementedError:
                return {'error': 'Unable to decrypt the PDF file.'}

        # Создаем словарь, в который будем сохранять информацию из файла
        pdf_info = {}

        # Получаем количество страниц в файле
        num_pages = len(pdf_reader.pages)
        pdf_info['num_pages'] = num_pages

        # Читаем каждую страницу и сохраняем текст в словарь
        for page_number, page in enumerate(pdf_reader.pages):
            text = page.extract_text()
            page_info = {}

            # Общие правила для полей авиабилета
            field_rules = {
                'PN': ['PN:'],
                'SN': ['SN:'],
                'DESCRIPTION': ['DESCRIPTION:'],
                'LOCATION': ['LOCATION:', 'LOCATION :'],
                'CONDITION': ['CONDITION:', 'CONDITION :'],
                'RECEIVER#': ['RECEIVER#:', 'RECEIVER# :'],
                'UOM': ['UOM:', 'UOM :'],
                'EXP DATE': ['EXP DATE:', 'EXP DATE :'],
                'PO': ['PO:', 'PO :'],
                'CERT SOURCE': ['CERT SOURCE:'],
                'REC.DATE': ['REC.DATE:', 'REC.DATE :'],
                'MFG': ['MFG:', 'MFG :'],
                'BATCH#': ['BATCH#:', 'BATCH# :'],
                'DOM': ['DOM:', 'DOM :'],
                'REMARK': ['REMARK:', 'REMARK :'],
                'LOT#': ['LOT# :', 'LOT#:'],
                'Qty': ['Qty:'],
                'NOTES': ['NOTES:']
            }

            for field, rules in field_rules.items():
                field_value = None

                # Поиск значения поля в тексте
                for rule in rules:
                    if rule in text:
                        field_value = text.split(rule, 1)[1].split('\n', 1)[0].strip()
                        break

                # Разделение значения на отдельные поля, если требуется
                if field == 'SERVICE NAME' and field_value:
                    field_parts = field_value.split(' ')
                    page_info['SERVICE NAME'] = field_parts[0].strip()
                    if len(field_parts) > 1:
                        page_info['PN'] = field_parts[1].strip()
                elif field == 'PN' and field_value:
                    field_parts = field_value.split('SN:')
                    page_info['PN'] = field_parts[0].strip()
                    if len(field_parts) > 1:
                        page_info['SN'] = field_parts[1].strip()
                elif field == 'LOCATION' and field_value:
                    field_parts = field_value.split('CONDITION:')
                    page_info[field] = field_parts[0].strip()
                    if len(field_parts) > 1:
                        page_info['CONDITION'] = field_parts[1].strip()
                elif field == 'RECEIVER#' and field_value:
                    field_parts = field_value.split('UOM:')
                    page_info[field] = field_parts[0].strip()
                    if len(field_parts) > 1:
                        page_info['UOM'] = field_parts[1].strip()
                elif field == 'EXP DATE' and field_value:
                    field_parts = field_value.split('PO:')
                    page_info[field] = field_parts[0].strip()
                    if len(field_parts) > 1:
                        page_info['PO'] = field_parts[1].strip()
                elif field == 'REC.DATE' and field_value:
                    field_parts = field_value.split('MFG:')
                    page_info[field] = field_parts[0].strip()
                    if len(field_parts) > 1:
                        page_info['MFG'] = field_parts[1].strip()
                elif field == 'BATCH#' and field_value:
                    field_parts = field_value.split('DOM:')
                    page_info[field] = field_parts[0].strip()
                    if len(field_parts) > 1:
                        page_info['DOM'] = field_parts[1].strip()
                elif field == 'REMARK' and field_value:
                    field_parts = field_value.split('LOT#:')
                    page_info[field] = field_parts[0].strip()
                    if len(field_parts) > 1:
                        page_info['LOT#'] = field_parts[1].strip()
                elif field == 'Qty' and field_value:
                    field_parts = field_value.split('NOTES:')
                    page_info[field] = field_parts[0].strip()
                    if len(field_parts) > 1:
                        page_info['NOTES'] = field_parts[1].strip()
                else:
                    page_info[field] = field_value

            pdf_info[f'page_{page_number + 1}'] = page_info

    print(pdf_info)
    return pdf_info
