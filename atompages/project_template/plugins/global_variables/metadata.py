import os
import logging
import json

try: input=raw_input
except: pass

options_to_set = ["site_name", "site_description", "default_author", "contact_header"]

default_styles = {
            "font-family": "  'Lora', 'Times New Roman', serif",
            "font-size": "20px",
            "font-color": "#404040",
            "primary-color": "#333",
            "menu_background": "rgba(255,255,255,.4)",
            "title-text-transform": "lowercase",

            "header-min-height": "40%",
            "header-width": "100%",
            "header-background-img": "url('/static/img/header01.jpg')",

            "page-offset-height": "0",
            "content-max-width": "100%",
            "content-background-color": "white",
            "heading-font-family": "'Open Sans', 'Helvetica Neue', Helvetica, Arial, sans-serif",
        }

#impressum is mandatory in germany for most websites for identification puposes
impressum = {
    "name": "",
    "email": "",
    "street": "",
    "zip-code": "",
    "city": "",
}

hidden_links = ['home', 'impressum', 'index']

def get_options(project_root):
    try:
        with open(project_root+"/options.json", "r") as f:
            return json.loads(f.read())
    except Exception as e:
        print("Option file not available or invalid. Please fill them in now\n")

    options = {entry: input("%s: "%entry) for entry in options_to_set}
    options["styles"] = default_styles
    options["impressum"] = impressum
    options["hidden_links"] = hidden_links
    with open(project_root + "/options.json","w") as f:
        f.write(json.dumps(options, sort_keys=True, indent=4))
    return options



def return_variables(project_root, *args):
    return get_options(project_root)
