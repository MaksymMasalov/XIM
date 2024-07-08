def check_pdf_structure(template_info, test_info):
    template_keys = set(template_info.keys())
    test_keys = set(test_info.keys())

    missing_keys = template_keys - test_keys
    additional_keys = test_keys - template_keys

    if missing_keys:
        print(f"Missing keys: {missing_keys}")
    if additional_keys:
        print(f"Additional keys: {additional_keys}")

    return not missing_keys and not additional_keys
