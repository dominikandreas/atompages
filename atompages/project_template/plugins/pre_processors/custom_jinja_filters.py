import datetime

def datetimeformat(value, format='%H:%M / %d-%m-%Y'):
    t = datetime.datetime.fromtimestamp(value)
    return t.strftime(format)


def preprocess(project_root, pages, menu, lang):
    # Environment is the same for all pages, so we only need to set the
    # filters for the first page
    pages[0].env.filters["datetimeformat"] = datetimeformat
    pages[0].env.filters["reversed"] = reversed
