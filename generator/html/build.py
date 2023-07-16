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
    if data["doc_type"] != "generic kernel":
        print("Error: this script only works for generic kernel documentation")
        exit(1)

    path_links = ""
    for i, l in enumerate(data["doc_path"]):
        full = "/".join(data["doc_path"][:i+1])
        if i == len(data["doc_path"]) - 1:
            path_links += f'<a href="/{full}.html">{l}</a>'
        else:
            path_links += f'<a href="/{full}">{l}</a> / '
    
    cfiles = ""
    for i, ary in enumerate(data["reported_cfiles"]):
        file = "/".join(ary)
        cfiles += f"<a href=\"https://github.com/elydre/profanOS/blob/main/{file}\">{file}</a>"
        if i != len(data["reported_cfiles"]) - 1:
            cfiles += ", "
    
    hfiles = ""
    for ary in data["reported_hfiles"]:
        file = "/".join(ary)
        hfiles += f"<a href=\"https://github.com/elydre/profanOS/blob/main/include/kernel/{file}\">{file}</a>"

    return {
        "NAME": data["doc_name"],
        "TYPE": data["doc_type"],
        "DESCRIPTION": data["summary"],
        "C_FILES": cfiles,
        "H_FILES": hfiles,
        "SCR_PLUR": "s" if len(data["doc_path"]) > 1 else "",
        "HDR_PLUR": "s" if len(data["reported_hfiles"]) > 1 else "",
        "VERSION": data["version"],
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
