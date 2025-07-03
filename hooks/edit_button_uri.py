import logging

log = logging.getLogger('mkdocs')

def get_edit_url(src_path, edit_url_SCSTG, edit_url_SCSVS):
    if src_path.startswith("SCSVS"):
        edit_url = f"{edit_url_SCSVS}{src_path}"
        edit_url = edit_url.replace("main/SCSVS/controls", "main/controls/")
        edit_url = edit_url.replace("main/SCSVS/", "main/0.1/en/")
    elif src_path.startswith("SCSTG"):
        edit_url = f"{edit_url_SCSTG}{src_path}"
        edit_url = edit_url.replace("main/SCSTG/0x", "main/docs/0x")
        edit_url = edit_url.replace("main/SCSTG/", "main/")
    elif src_path.startswith("scwe"):
        edit_url = f"{edit_url_SCSTG}{src_path}"
        edit_url = edit_url.replace("main/scwe/", "main/weaknesses/")
    elif src_path.startswith(("contributing", "donate")):
        edit_url = f"{edit_url_SCSTG}{src_path}"
        edit_url = edit_url.replace("main/", "main/docs/")
    else:
        edit_url = ""
    
    return edit_url

def on_pre_page(page, config, files):
    try:
        edit_url_SCSTG = "https://github.com/OWASP/www-project-smart-contract-security-testing-guide/edit/master/"
        edit_url_SCSVS = "https://github.com/OWASP/www-project-smart-contract-security-verification-standard/edit/master/"
    except KeyError:
        return page
    
    src_path = page.file.src_path

    if src_path.startswith(("SCSTG", "SCSVS", "scwe", "contributing", "donate")):
        edit_url = get_edit_url(src_path, edit_url_SCSTG, edit_url_SCSVS)
        if edit_url.endswith("/index.md"):
            page.edit_url = ""
        else:
            page.edit_url = edit_url
    else:
        page.edit_url = ""
 
    return page