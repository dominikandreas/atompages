

def return_variables(project_root, pages, menu, lang):
    recently_created = sorted(pages, key = lambda p:p.ctime)
    recently_modified =  sorted(pages, key = lambda p:p.mtime)
    sorted_by_date = sorted(pages, key = lambda p: p.date)
    return {"recently_modified": recently_modified,
            "recently_created": recently_created,
            "sorted_by_date":sorted_by_date}
