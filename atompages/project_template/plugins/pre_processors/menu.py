from ..global_variables import metadata


def hide_from_menu(menu, exclusion):
    return [entry for entry in menu if not exclusion in entry]

def preprocess(project_root, pages, menu, lang):
    #remove links to hide
    for exclusion in metadata.get_options(project_root)["hidden_links"]:
        menu[:] = hide_from_menu(menu, exclusion)[:]
        for page in pages:
            if page.name.lower() == exclusion.lower():
                page.hidden_link = True

    # create category menu
    categories = {}
    for page in pages:
        if not page.category == "default":
            categories[page.category] = categories.get(page.category,[]).append(page)
    if not len(categories) == 0:
        menu["categories"] = [[category, entries] for category, entries in categories.items()]
