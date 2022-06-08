

def remove_none_values(dict_to_clean: dict):
    temp_dict = {}

    for k, v in dict_to_clean.items():
        if v is not None:
            temp_dict[k] = v

    return temp_dict


def sort_pages(pages: dict):
    results = []

    for k, v in pages.items():
        results.append((k, v))

    results.sort(reverse=False, key=lambda x: x)

    return results


def print_report(pages):
    clean_pages = remove_none_values(pages)
    sorted_pages = sort_pages(clean_pages)
    for url, count in sorted_pages:
        print(f"Found {count} internal links to {url}")
