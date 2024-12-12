import logging
import mkdocs.plugins

log = logging.getLogger('mkdocs')

checklists_banner = """
!!! info "Temporary Checklist"
    This checklist contains the **SCSVS v0.0.1 verification levels (L1, L2 and L3)** which we are currently reworking into "security testing profiles". The levels were assigned according to the SCSVS v1 ID that the test was previously covering and might differ in the upcoming version of the SCSTG and SCS Checklist.

    For the upcoming of the SCSTG version we will progressively split the SCSTG tests into smaller tests, the so-called "atomic tests" and assign the new [SCS profiles](https://docs.google.com/document/d/1IdJbabgOaA6cIiCbxoEnZYOvHt-pidOsNtZGRZ659UY/edit?usp=sharing) to their respective SCWE weaknesses.
"""

# https://www.mkdocs.org/dev-guide/plugins/#on_page_markdown
@mkdocs.plugins.event_priority(-50)
def on_page_markdown(markdown, page, **kwargs):
    path = page.file.src_uri

    if "checklists/SCSVS-" in path:
        markdown = "\n" + checklists_banner + "\n\n" + markdown

    return markdown
