"""
Enriches docs/assets/data/scs-checklist.yaml with VR ID (rid) from scsvs.yaml.
Runs at pre-build so the interactive checklist displays the canonical rid (e.g. S1.1.A1).
"""
import logging
import os
import yaml

log = logging.getLogger('mkdocs')

# Paths relative to project root (where mkdocs runs)
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DOCS_DIR = os.path.normpath(os.path.join(SCRIPT_DIR, '..'))


def get_rid_list_from_scsvs(scsvs_path):
    """Build ordered list of (gid, rid, testname, cid) from scsvs.yaml."""
    if not os.path.exists(scsvs_path):
        log.warning(f"add_rid_to_checklist: {scsvs_path} not found")
        return []
    with open(scsvs_path, 'r') as f:
        data = yaml.safe_load(f)
    if not data or 'groups' not in data:
        return []
    result = []
    for group in data['groups']:
        gid = group.get('gid', '')
        for ctrl in group.get('controls', []):
            cid = ctrl.get('cid', '')
            for req in ctrl.get('requirements', []):
                rid = req.get('rid', '')
                testname = (req.get('testname', '') or '').strip()
                result.append((gid, rid, testname, cid))
    return result


def enrich_checklist_with_rid(config):
    """Add rid to each item in scs-checklist.yaml by matching from scsvs."""
    docs_dir = config.get('docs_dir', DOCS_DIR)
    if not os.path.isabs(docs_dir):
        docs_dir = os.path.join(os.getcwd(), docs_dir)
    scsvs_path = os.path.join(docs_dir, 'SCSVS', 'scsvs.yaml')
    checklist_path = os.path.join(docs_dir, 'assets', 'data', 'scs-checklist.yaml')

    if not os.path.exists(checklist_path):
        log.warning(f"add_rid_to_checklist: {checklist_path} not found")
        return

    rid_list = get_rid_list_from_scsvs(scsvs_path)
    if not rid_list:
        return

    # Build index: gid -> [(rid, testname, cid), ...] in order
    by_gid = {}
    for gid, rid, testname, cid in rid_list:
        by_gid.setdefault(gid, []).append({'rid': rid, 'testname': testname, 'cid': cid})

    with open(checklist_path, 'r') as f:
        checklist = yaml.safe_load(f)

    if not checklist or 'categories' not in checklist:
        return

    updated = 0
    for cat in checklist.get('categories', []):
        gid = cat.get('id', '')
        reqs = by_gid.get(gid, [])
        if not reqs:
            continue
        for idx, item in enumerate(cat.get('items', [])):
            if idx < len(reqs) and item.get('rid') != reqs[idx]['rid']:
                item['rid'] = reqs[idx]['rid']
                updated += 1

    if updated == 0:
        return
    with open(checklist_path, 'w') as f:
        yaml.dump(checklist, f, default_flow_style=False, allow_unicode=True, sort_keys=False)

    log.info(f"add_rid_to_checklist: added rid to {updated} items")


def on_pre_build(config, **kwargs):
    try:
        enrich_checklist_with_rid(config)
    except Exception as e:
        log.warning(f"add_rid_to_checklist: {e}")
