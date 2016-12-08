
def preprocess(project_root, pages, menu, lang):
    for page, prev, next in zip(pages[1:-1],pages[:-2],pages[2:]):
        page.update_vars(prev=prev, next=next)
    pages[0].update_vars(next=pages[1])
    pages[-1].update_vars(prev=pages[-2])
