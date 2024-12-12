import logging
import yaml
import mkdocs.plugins
import glob, os
from collections import defaultdict

log = logging.getLogger('mkdocs')

def get_cg_tests_data():

    scsvs_cg_tests_metadata = {}
    # Each test has an ID which is the filename
    for file in glob.glob("./tests/**/*.md", recursive=True):
        if "index.md" not in file:
            try:
                with open(file, 'r') as f:
                    content = f.read()
                    frontmatter = next(yaml.load_all(content, Loader=yaml.FullLoader))
                    # SCSVS category is frontmatter['SCSVS_cg_id'][0] without the final number. Example: SCSVS-ARCH-2 -> SCSVS-ARCH
                    scsvs_category = frontmatter['scsvs_scg_id'][0][:-2]
                    platform = frontmatter['platform']
                    # get id from filename without extension
                    id = file.split('/')[-1].split('.')[0]
                    link = f"https://scs.owasp.org/SCSTG/tests/{scsvs_category}/{id}/"
                    frontmatter['link'] = link
                    
                    scsvs_cg_tests_metadata[id] = frontmatter
            except:
                log.warn("No frontmatter in " + file)

    # Populate the defaultdict with SCSVS v1 IDs and corresponding SCSTG-TEST IDs
    scsvs_cg_mapping = defaultdict(list)
    for test_id, test_info in scsvs_cg_tests_metadata.items():
        for scsvs_id in test_info["scsvs_cg_id"]:
            scsvs_cg_mapping[scsvs_id].append(f"[{test_id}]({test_info['link']})")

    return scsvs_cg_tests_metadata, scsvs_cg_mapping

beta_banner = """
??? example "Content in BETA"
    This content is in **beta** and still under active development, so it is subject to change any time (e.g. structure, IDs, content, URLs, etc.).
    
    [:fontawesome-regular-paper-plane: Send Feedback](https://github.com/OWASP/owasp-scstg/discussions/categories/scwe-scstg-v2-beta-feedback)
"""

def get_scstg_cg_coverage(meta):
    mappings = meta.get('mappings', '')

    if mappings:
        scstg_cg_tests_metadata, scstg_cg_mapping = get_cg_tests_data()

        scsvs_cg_id = mappings.get('scsvs-cg', '')
        if len(scsvs_cg_id) > 1:
            raise ValueError(f"More than one SCSVS CG ID found: {scsvs_cg_id}")
        scsvs_cg_id = scsvs_cg_id[0] if scsvs_cg_id else ""
        scstg_cg_tests_map = scstg_cg_mapping.get(scsvs_cg_id, [])

        scstg_cg_tests_map_list = [f"{test.split(']')[0].split('[')[1]}" for test in scstg_cg_tests_map]
        mappings['scstg-cg'] = scstg_cg_tests_map_list

        scstg_cg_tests = "\n".join([f"    - [{test} - {scstg_cg_tests_metadata[test]['title']} ({scstg_cg_tests_metadata[test]['platform']})]({scstg_cg_tests_metadata[test]['link']})" for test in scstg_cg_tests_map_list])
        if scstg_cg_tests == "":
            scstg_cg_tests = "    No SCSTG CG tests are related to this weakness."
    return scstg_cg_tests

def get_info_banner(meta):

    id = meta.get('id')

    refs = meta.get('refs', None)
    refs_section = ""
    if refs:
        refs_section = "    ## References\n\n"
        refs_section += "\n".join([f"    - <{ref}>" for ref in refs])

    draft_info = meta.get('draft', None)

    description = draft_info.get('description', None)

    if draft_info.get('note', None):
        description += "\n\n" + "    > Note: " + draft_info.get('note', None) + "\n"

    topics = draft_info.get('topics', None)
    topics_section = ""
    if topics:
        topics_section = "    ## Relevant Topics\n\n"
        topics_section += "\n".join([f"    - {topic}" for topic in topics])
    
    scstg_cg_tests = get_scstg_cg_coverage(meta)

    info_banner = f"""
!!! warning "Draft Weakness"

    This weakness hasn't been created yet and it's in **draft**. But you can check its status or start working on it yourself.
    If the issue has not yet been assigned, you can request to be assigned to it and submit a PR with the new content for that weakness by following our [guidelines](https://docs.google.com/document/d/1EMsVdfrDBAu0gmjWAUEs60q-fWaOmDB5oecY9d9pOlg/edit?usp=sharing).

    <a href="https://github.com/OWASP/owasp-scstg/issues?q=is%3Aissue+is%3Aopen+{id}" target="_blank">:material-github: Check our GitHub Issues for {id}</a>
    
    ## Initial Description or Hints

    {description}
    
{topics_section}
    
{refs_section}

    ## SCSTG CG Coverage

{scstg_cg_tests}
"""
    return info_banner

# https://www.mkdocs.org/dev-guide/plugins/#on_page_markdown
@mkdocs.plugins.event_priority(-50)
def on_page_markdown(markdown, page, **kwargs):
    path = page.file.src_uri

    banners = []

    if any(substring in path for substring in ["SCWE/", "SCSTG/tests-beta/"]):
        banners.append(beta_banner)
    
    if "SCWE/" in path and page.meta.get('status') == 'draft':
        banners.append(get_info_banner(page.meta))

    if banners:
        markdown = "\n\n".join(banners) + "\n\n" + markdown

    return markdown
