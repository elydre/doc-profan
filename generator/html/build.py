import json
import os


def get_json_data(path):
    with open(path, "r") as f:
        data = json.load(f)
    return data

def get_output_path(path):
    return os.path.join("build", path) + ".html"

def get_json_path(path):
    return os.path.join("source", path) + ".json"

def get_template():
    with open("generator/html/template.html", "r") as f:
        template = f.read()
    return template

def generate_repdict(data):
    path_links = ""
    for i, l in enumerate(data["doc_path"]):
            full = "/".join(data["doc_path"][:i+1])
            if i == len(data["doc_path"]) - 1:
                path_links += f'<a href="/{full}.html">{l}</a>'
            else:
                path_links += f'<a href="/{full}">{l}</a> / '

    return {
        "NAME": data["doc_name"],
        "PATH_LINKS": path_links,
    }

def generate_html(template, repdict):
    for key, value in repdict.items():
        template = template.replace("{" + key + "}", value)
    return template

def write_html(path, html):
    with open(path, "w") as f:
        f.write(html)

path = "kernel/process"
data = get_json_data(get_json_path(path))
template = get_template()
repdict = generate_repdict(data)
html = generate_html(template, repdict)
write_html(get_output_path(path), html)
