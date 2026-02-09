import logging
import re
import mkdocs.plugins
import os
from glob import glob
import yaml

log = logging.getLogger('mkdocs')

mapping = {"TECH":{}, "TOOL":{}, "TEST": {}, "APP": {}, "SCWE": {}, "SCSVS": {}, "DEMO": {}, "MITIG": {}}

@mkdocs.plugins.event_priority(-50)
def on_page_markdown(markdown, page, config, **kwargs):
    path = page.file.src_uri

    icons = config.get('theme').get('icon').get('tag', {})

    icons_for_text = {key.upper(): f":{value.replace('/', '-')}: " for key, value in icons.items()}

    pageRefs = {"TECH": [], "TOOL": [], "TEST": [], "APP": [], "SCWE": [], "SCSVS": [], "DEMO": [], "MITIG": []}
    
    def replaceReference(match):
        refType = match.group(2)

        pageRefs[refType].append(match.group(1))

        if not match in mapping[refType]:
            target = getTargetForRef(match.group(1), path)
            mapping[refType][match] = target

        icon = icons_for_text.get(refType, ":octicons-question-24: ")

        return f"_[{icon}{mapping[refType][match]['title']}]({mapping[refType][match]['file']})_"

    def replaceReferenceSCWE(match):
        refType = "SCWE"

        pageRefs[refType].append(match.group(1))

        if not match in mapping[refType]:
            target = getTargetForRef(match.group(1), path)
            mapping[refType][match] = target

        icon = icons_for_text.get(refType, ":octicons-question-24: ")
        return f"_[{icon}{mapping[refType][match]['title']}]({mapping[refType][match]['file']})_"

    def replaceReferenceSCSVS(match):
        refType = "SCSVS"

        pageRefs[refType].append(match.group(1))

        if not match in mapping[refType]:
            target = getTargetForRef(match.group(1), path)
            mapping[refType][match] = target

        icon = icons_for_text.get(refType, ":octicons-question-24: ")
        return f"_[{icon}{mapping[refType][match]['title']}]({mapping[refType][match]['file']})_"


    updated_markdown = re.sub(r'@(SCSTG-(TEST|TOOL)-\d{3,})', replaceReference, markdown)
    updated_markdown = re.sub(r'@(SCWE-\d{3,})', replaceReferenceSCWE, updated_markdown)
    updated_markdown = re.sub(r'@(SCSVS-\w+)', replaceReferenceSCSVS, updated_markdown)

    return updated_markdown

def getTargetForRef(id, path):
    searchFor = f'./docs/**/{id}.md'

    files = glob(searchFor, recursive=True)

    if not len(files):
        log.error("Unknown reference: " + id)
        return {"file": "ERROR", "title": "error"}
    
    file_url =   os.path.relpath(files[0], "./docs/" + os.path.dirname(path))

    with open(files[0], 'r') as f:
        content = f.read()
        metadata = next(yaml.safe_load_all(content))

        return {"file": file_url, "title": metadata['title']}
