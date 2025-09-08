import logging
import mkdocs.plugins

log = logging.getLogger('mkdocs')

# https://www.mkdocs.org/dev-guide/plugins/#on_page_markdown
@mkdocs.plugins.event_priority(-50)
def on_page_markdown(markdown, page, **kwargs):
    path = page.file.src_uri

    tags = page.meta.get('tags', [])

    if page.meta.get('scsvs_category'):
        tags.append(page.meta.get('scsvs_category'))
        
    if page.meta.get('platform'):
        if type(page.meta.get('platform')) == str:
            tags.append(page.meta.get('platform'))
        elif type(page.meta.get('platform')) == list:
            for platform in page.meta.get('platform'):
                tags.append(platform)    

    if page.meta.get('profiles'):
        for profile in page.meta.get('profiles', []):
            tags.append(profile)

    if page.meta.get('weakness'):
        tags.append(page.meta.get('weakness'))
    if page.meta.get('test'):
        tags.append(page.meta.get('test'))
    
    if mappings:=page.meta.get('mappings'):
        if scsvs_cg:=mappings.get('scsvs-cg'):
            for scsvs_id in scsvs_cg:
                tags.append(scsvs_id)
        if scsvs_scg:=mappings.get('scsvs-scg'):
            for scsvs_id in scsvs_scg:
                tags.append(scsvs_id)
                
    # TODO - This is only for the SCSTG v1 tests; remove this once all pages have been updated to use mappings
    if scsvs_scg:=page.meta.get('scsvs_scg_id'):
        for scsvs_id in scsvs_scg:
            tags.append(scsvs_id)
    if scsvs_cg:=page.meta.get('scsvs_cg_id'):
        for scsvs_id in scsvs_cg:
            tags.append(scsvs_id)
    # END TODO

    if page.meta.get('status'):
        if page.meta.get('status') == 'draft':
            tags.append('draft')
    
    page.meta['tags'] = tags

    return markdown
