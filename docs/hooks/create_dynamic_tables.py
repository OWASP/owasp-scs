import pandas
import yaml
import os
import glob
import mkdocs
from pathlib import Path
import yaml
import re
import logging

import requests
log = logging.getLogger('mkdocs')
SCSVS = None

def get_platform(input_file: str) -> str:
    if "/android/" in input_file:
        return "android"
    elif "/ios/" in input_file:
        return "ios"




def get_scstg_tests_dict():
    scstg_tests = {}

    # Iterate over all markdown files in the specified directory
    for file in glob.glob("docs/SCSTG/tests/**/*.md", recursive=True):
        if "index.md" not in file:
            print(f"\nProcessing file: {file}")  # Debugging line: prints the current file being processed
            with open(file, 'r') as f:
                id = ""
                content = f.read()
                try:
                    # Load the frontmatter from the markdown file
                    frontmatter = next(yaml.load_all(content, Loader=yaml.FullLoader))
                    print(f"Loaded frontmatter: {frontmatter}")  # Debugging line: prints the loaded frontmatter

                    # Extract scsvs_cg_id
                    scsvs_scg_id = frontmatter['scsvs_scg_id']
                    frontmatter['path'] = os.path.relpath(file, "docs/SCSTG")
                    if scsvs_scg_id:
                        id = scsvs_scg_id[0] 
                        if id not in scstg_tests:
                            scstg_tests[id] = {}
                        print(f"Found SCSVS-SCG ID: {id}")  # Debugging line: prints the scsvs_cg_id

                        # Extract SCSTG TEST ID from the filename
                        SCSTG_TEST_ID = re.compile(r".*(SCSTG-TEST-\d*).md$").match(file).group(1)
                        print(f"Extracted SCSTG TEST ID: {SCSTG_TEST_ID}")  # Debugging line: prints the SCSTG TEST ID
                        frontmatter['SCSTG-TEST-ID'] = SCSTG_TEST_ID
                    else:
                        print(f"No SCSVS coverage for: {frontmatter['title']} (was {frontmatter['scsvs_cg_id']})")
                except StopIteration:
                    print(f"Error reading file {file}. Skipping.")  # Debugging line: print an error if YAML parsing fails
                    continue
    return scstg_tests


def retrieve_scsvs():
    global SCSVS
    file_path = "docs/SCSVS/scsvs.yaml"
    
    # Check if the file exists before trying to open it
    if not os.path.exists(file_path):
        print(f"File {file_path} not found!")
        return None
    try:
        with open(file_path, 'r') as file:
            content = file.read()
            print("YAML content loaded successfully:", "\n")
            print(content)  # Print the raw YAML content to inspect it
            
            SCSVS = yaml.safe_load(content)
            
            if SCSVS is None:
                print("Failed to parse YAML content.")
                return None
            
            # Debugging: Inspect if data is loaded correctly
            print("Parsed YAML content:", "\n")
            print(SCSVS)  # Print the parsed structure
            
            # Check for missing 'objective' key in controls
            for group in SCSVS.get('groups', []):
                for control in group.get('controls', []):
                    if 'objective' not in control:
                        print(f"Missing 'objective' in control {control.get('cid')}")
            
    except Exception as e:
        print(f"Error loading YAML file: {e}")
        return None

    return SCSVS


def get_scsvs_groups():
    groups = {}
    for group in SCSVS['groups']:
        group_id = group['gid']
        groups[group_id] = {'gid': group_id, 'title': group['title']}
    return groups



def add_control_row(checklist, control):
    grouped_by_rid = {}  # Dictionary to store questions grouped by 'rid'
    
    # Loop through each requirement
    for req in control.get('requirements', []):
        rid = req['rid']
        
        # Check if the 'rid' is already in the grouped_by_rid dictionary
        if rid not in grouped_by_rid:
            grouped_by_rid[rid] = {
                'questions': [],
                'control_id': control['cid'],
                'testname': req['testname'],
                'test_id': req.get('tid', 'No Test ID'),
                'path': f"./SCSVS/controls/{os.path.basename(control['cid'])}"
            }

        # Loop through the checklist questions and append them to the list
        for question in req.get('checklist', []):
            grouped_by_rid[rid]['questions'].append(question)

    # Now, generate the rows based on grouped questions by 'rid'
    for rid, group in grouped_by_rid.items():
        checklist_row = {}
        
        # Add the control ID to the row
        checklist_row['SCG ID'] = group['control_id']
        print(f"Added Control ID for VR ID {rid}: {checklist_row['SCG ID']}")  # Debugging
        
        # Add the current 'rid' to the row
        checklist_row['VR ID'] = rid
        print(f"Added VR ID {rid}")  # Debugging: Confirm each VR ID was added
        checklist_row['path'] = group['path']

        # Add the test ID ('tid') to the row and append the test_path if available
        test_path = f"../../SCSTG/tests/" if group['test_id'] != 'No Test ID' else ''
        checklist_row['TEST ID'] = f"[{group['test_id']}]({test_path})" if test_path else 'No Test ID'
        print(f"Added TEST ID for VR ID {rid}: {checklist_row['TEST ID']}")  # Debugging
        
        # Add the specific 'requirement' (control statement) for each rid
        checklist_row['Control / SCSTG Test'] = group['testname']
        print(f"Added Control / SCSTG Test for VR ID {rid}: {checklist_row['Control / SCSTG Test']}")  # Debugging
        
        # Combine all checklist questions for this VR ID into a single string with bullet points
        checklist_row['Checklist'] = "\n".join([f"- {question}" for question in group['questions']]) if group['questions'] else "No checklist available."
        
        # Append the row to the checklist
        checklist.append(checklist_row)
        print(f"Checklist after addition for VR ID {rid}: {checklist}")  # Debugging: Output the updated checklist





def add_test_rows(checklist, platform, control):

    print("\n", "Adding tests:", control)  # Debugging line to print all SCSTG tests
    
    if platform in control['tests']:
        print(f"\nPlatform '{platform}' found in tests.")  # Debugging line to confirm platform is found
        for test in control['tests'][platform]:
            print("\n", "Test ID:", test['SCSTG-TEST-ID'])  # Debugging line to output the test ID

            # Debugging: Show the test details
            print("Test Details:", test)

            levels = test['scsvs_cg_levels']
            print("Levels for this test:", levels)  # Debugging line to see the levels for the current test

            checklist_row = {}
            checklist_row['SCG ID'] = ""
            checklist_row['Control / SCSTG Test'] = test['title']
            checklist_row['SCSTG-TEST-ID'] = test["SCSTG-TEST-ID"]
            checklist_row['path'] = f"/SCSTG/{os.path.splitext(test['path'])[0]}"
            # Debugging: Output the assignment of the L1, L2, R levels
            checklist_row['L1'] = "L1" in levels
            checklist_row['L2'] = "L2" in levels
            checklist_row['R'] = "R" in levels
            print(f"Assigned Levels -> L1: {checklist_row['L1']}, L2: {checklist_row['L2']}, R: {checklist_row['R']}")  # Debugging levels assignment
            print("Test Details:", test)

            checklist.append(checklist_row)
            print(f"Checklist after adding test {test['SCSTG-TEST-ID']}:", checklist)  # Debugging line to show the checklist after each addition
            

def get_checklist_dict():
    print("\nFetching SCSVS data...")  # Debugging line to indicate start of retrieval
    scsvs_scg = retrieve_scsvs()
    print("\n", "Parsed SCSVS:", scsvs_scg)  # Debugging line to inspect the parsed SCSVS data

    print("\nFetching SCSTG tests...")  # Debugging line to indicate start of retrieval for SCSTG tests
    scstg_tests = get_scstg_tests_dict()
    print("\n", "Loaded SCSTG Tests:", scstg_tests)  # Debugging line to check the loaded SCSTG tests

    checklist_dict = {}

    # Loop through SCSVS groups
    for group in scsvs_scg['groups']:
        print(f"\nProcessing Group: {group['gid']}")  # Debugging line to show which group is being processed
        checklist_per_group = []

        # Loop through controls in each group
        for control in group['controls']:
            print(f"\nProcessing Control: {control['cid']}")  # Debugging line to show the current control being processed
            add_control_row(checklist_per_group, control)  # Adding control row to checklist

            control_id = control['cid']
            print(f"Control ID: {control_id}")  # Debugging: show control ID for testing against SCSTG tests

            # Check if there are SCSTG tests associated with this control
            if control_id in scstg_tests:
                print(f"Found SCSTG tests for Control ID: {control_id}")  # Debugging: Confirm SCSTG tests are present
                control['tests'] = scstg_tests[control_id]
                
                # Adding tests for Android platform
                print(f"Adding tests for Android platform...")  # Debugging: indicate addition of Android tests
                add_test_rows(checklist_per_group, "android", control)

                # Adding tests for iOS platform
                print(f"Adding tests for iOS platform...")  # Debugging: indicate addition of iOS tests
                add_test_rows(checklist_per_group, "ios", control)

        # After processing all controls in the group, add it to the checklist dictionary
        checklist_dict[group['gid']] = checklist_per_group
        print(f"Finished processing Group {group['gid']}. Added {len(checklist_per_group)} controls.")  # Debugging: Group completion
         # Final checklist dictionary after processing all groups
        print("\nFinal checklist dictionary:", checklist_dict)  # Debugging: Output the final checklist dictionary
    return checklist_dict



CHECKLIST_DICT = {}
def on_pre_build(config):
    global CHECKLIST_DICT
    CHECKLIST_DICT = get_checklist_dict()
    print("\n", "Checklist Dictionary Created:", CHECKLIST_DICT)  # Debugging line
    print("Available keys in CHECKLIST_DICT:", CHECKLIST_DICT.keys())


def get_platform_icon(platform):
    if platform == "android":
        return '<span style="font-size: x-large; color: #54b259;" title="Android"> :material-android: </span><span style="display: none;">platform:android</span>'
    elif platform == "ios":
        return '<span style="font-size: x-large; color: #007aff;" title="iOS"> :material-apple: </span><span style="display: none;">platform:ios</span>'
    elif platform == "generic":
        return '<span style="font-size: x-large; color: darkgrey;" title="Generic"> :material-asterisk: </span><span style="display: none;">platform:generic</span>'
    elif platform == "network":
        return '<span style="font-size: x-large; color: #9383e2;" title="Network"> :material-web: </span><span style="display: none;">platform:network</span>'
    else:
        return '<span style="font-size: x-large; color: darkgrey;" title="Unknown"> :material-progress-question: </span><span style="display: none;">platform:unknown</span>'



def get_level_icon(level, value):
    if level == "L1" and value == True:
        return '<span class="SCS-dot-blue"></span><span style="display: none;">profile:L1</span>'
    elif level == "L2" and value == True:
        return '<span class="SCS-dot-green"></span><span style="display: none;">profile:L2</span>'
    elif level == "R" and value == True:
        return '<span class="SCS-dot-orange"></span><span style="display: none;">profile:R</span>'
    elif level == "P" and value == True:
        return '<span class="SCS-dot-purple"></span><span style="display: none;">profile:P</span>'

def set_icons_for_web(checklist):

    for row in checklist:
        # if it's a control row, make the SCG ID and Control bold
        if row['SCG ID'] != "":
            relPath = os.path.relpath(row['path'], './checklists/') + ".md"
            row['SCG ID'] = f"**[{row['SCG ID']}]({relPath})**"
            row['Control / SCSTG Test'] = f"**{row['Control / SCSTG Test']}**"
            
        # if it's a test row, set the icons for platform and levels
        else:
            
            row['Control / SCSTG Test'] = f"@{row['SCSTG-TEST-ID']}"
            row['L1'] = get_level_icon('L1', row['L1'])
            row['L2'] = get_level_icon('L2', row['L2'])
            row['R'] = get_level_icon('R', row['R'])        

def list_of_dicts_to_md_table(data, column_titles=None, column_align=None):
    if column_titles is None: column_titles = {key:key.title() for (key,_) in data[0].items()}
    df = pandas.DataFrame.from_dict(data).rename(columns=column_titles)
    return df.to_markdown(index=False, colalign=column_align)


def append_to_page(markdown, new_content):

    return markdown + "\n"+ new_content + "\n\n<br>\n\n"


def get_scstg_components_dict(name):
    
        components = []
    
        for file in glob.glob(f"{name}/**/*.md", recursive=True):
            if "index.md" not in file:
                with open(file, 'r') as f:
                    content = f.read()
        
                    frontmatter = next(yaml.load_all(content, Loader=yaml.FullLoader))
                    component_id = os.path.splitext(os.path.basename(file))[0]
                    component_path = os.path.splitext(os.path.relpath(file, "docs/"))[0]
                    frontmatter['id'] = component_id
                    frontmatter['title'] = f"@{component_id}"
                    if frontmatter.get('platform') and type(frontmatter['platform']) == list:
                        frontmatter['platform'] = "".join([get_platform_icon(platform) for platform in frontmatter['platform']])
                    else:
                        frontmatter['platform'] = get_platform_icon(frontmatter['platform'])
                    components.append(frontmatter)
                    components.append(frontmatter)
        return components


def get_all_weaknesses():
    weaknesses = []

    for file in glob.glob("docs/SCWE/**/SCWE-*.md", recursive=True):
        print("\nProcessing file:", file)  # Debugging line
        
        with open(file, 'r') as f:
            content = f.read()
            print("Read file content.")  # Debugging line
            
            try:
                frontmatter = next(yaml.load_all(content, Loader=yaml.FullLoader))
                print("Parsed YAML frontmatter:", frontmatter)  # Debugging line
            except StopIteration:
                print(f"Error: No valid YAML frontmatter found in {file}. Skipping this file.")
                continue
            
            # Ensure all required keys exist in frontmatter
            required_keys = ['id', 'title', 'platform', 'mappings', 'profiles']
            for key in required_keys:
                if key not in frontmatter:
                    print(f"Error: Missing key '{key}' in file {file}. Skipping this file.")
                    continue
            
            # Construct additional properties
            frontmatter['path'] = f"/SCWE/{os.path.splitext(os.path.relpath(file, 'docs/SCWE'))[0]}"
            print("Constructed path:", frontmatter['path'])  # Debugging line
            weaknesses_id = frontmatter['id']
            frontmatter['id'] = weaknesses_id
            frontmatter['title'] = f"@{frontmatter['id']}"
            print("Assigned title:", frontmatter['title'])  # Debugging line
            frontmatter['scsvs_scg_id'] = frontmatter['mappings']['scsvs-scg'][0]
            frontmatter['scsvs_cg_id'] = frontmatter['mappings']['scsvs-cg'][0]
            frontmatter['scsvs_category'] = frontmatter['scsvs_scg_id'][:frontmatter['scsvs_scg_id'].rfind('-')]
            print("Extracted SCSVS mappings:", frontmatter['scsvs_scg_id'], frontmatter['scsvs_cg_id'], frontmatter['scsvs_category'])  # Debugging line

            
            # Assign levels and profiles
            frontmatter['L1'] = get_level_icon('L1', "L1" in frontmatter['profiles'])
            frontmatter['L2'] = get_level_icon('L2', "L2" in frontmatter['profiles'])
            frontmatter['R'] = get_level_icon('R', "R" in frontmatter['profiles'])
            frontmatter['P'] = get_level_icon('P', "P" in frontmatter['profiles'])
            print("Assigned levels:", frontmatter['L1'], frontmatter['L2'], frontmatter['R'], frontmatter['P'])  # Debugging line
            
            # Handle status
            frontmatter['status'] = frontmatter.get('status', 'new')
            status = frontmatter['status']
            if status == 'new':
                frontmatter['status'] = '<span class="md-tag md-tag-icon md-tag--new">new</span><span style="display: none;">status:new</span>'
            elif status == 'draft':
                frontmatter['status'] = f'<a href="https://github.com/OWASP/www-project-smart-contract-security-testing-guide/issues?q=is%3Aissue+is%3Aopen+{frontmatter["id"]}" target="_blank"><span class="md-tag md-tag-icon md-tag--draft" style="min-width: 4em">draft</span></a><span style="display: none;">status:draft</span>'
            elif status == 'deprecated':
                frontmatter['status'] = '<span class="md-tag md-tag-icon md-tag--deprecated">deprecated</span><span style="display: none;">status:deprecated</span>'
            
            # Assign platform icons
            frontmatter['platform'] = "".join([get_platform_icon(platform) for platform in frontmatter['platform']])
            print("Assigned status and platform:", frontmatter['status'], frontmatter['platform'])  # Debugging line
            
            # Append to weaknesses list
            weaknesses.append(frontmatter)
            print("Weakness added to list.")  # Debugging line
            
    print("\nFinal weaknesses list:", weaknesses)  # Debugging line
    return weaknesses








def reorder_dict_keys(original_dict, key_order):
    return {key: original_dict.get(key, "N/A") for key in key_order}



# Higher priority, so that tables are parsed by the other hooks too
@mkdocs.plugins.event_priority(50)
def on_page_markdown(markdown, page, **kwargs):

    path = page.file.src_uri

    if path.endswith('/tests/index.md'):

        # Column titles for the table
        column_titles = {
            'id': 'TEST ID', 
            'title': 'Title',  
            'scsvs_cg_id': "SCSVS CG ID", 
            'scsvs_scg_id': "SCSVS SCG IDs", 
            'last_updated': 'Last Updated'
        }

        # Fetching the test components
        tests = get_scstg_components_dict("docs/SCSTG/tests")
        
        # Reorder the keys based on column_titles
        tests_of_type = [reorder_dict_keys(test, column_titles.keys()) for test in tests]
        print("Tests after reordering keys:", tests_of_type)  # Debugging line

        # Remove duplicates by test ID
        seen_test_ids = set()
        unique_tests = []
        
        for test in tests_of_type:
            test_id = test.get("id")
            if test_id and test_id not in seen_test_ids:
                seen_test_ids.add(test_id)
                unique_tests.append(test)

        # Now process the tests to update the 'scsvs_scg_id' and 'scsvs_cg_id' fields
        for test in unique_tests:
            if test.get("scsvs_scg_id"):
                test['scsvs_scg_id'] = test['scsvs_scg_id'][0]
            if test.get("scsvs_cg_id"):
                test['scsvs_cg_id'] = "<br>".join([f"{cg_id}" for cg_id in test['scsvs_cg_id']])

        # Append to page with the modified unique tests
        return append_to_page(markdown, list_of_dicts_to_md_table(unique_tests, column_titles))




    elif path.endswith("SCWE/index.md"):
        # weaknesses/index.md

        column_titles = {'id': 'SCWE ID', 'title': 'Title',   'scsvs_cg_id': "SCSVS CG ID",  'scsvs_scg_id': "SCSVS SCG IDs", 'L1': 'L1', 'L2': 'L2', 'status': 'Status'}

        weaknesses = get_all_weaknesses()
        weaknesses_columns_reordered = [reorder_dict_keys(weakness, column_titles.keys()) for weakness in weaknesses]

        return append_to_page(markdown, list_of_dicts_to_md_table(weaknesses_columns_reordered, column_titles) )

    elif path.endswith("talks.md"):
        # talks.md

        data = yaml.safe_load(open("docs/assets/data/talks.yaml"))

        for element in data:
            if element['video'].startswith("http"):
                element['video'] = f"[:octicons-play-24: Video]({element['video']})"
            if element['slides'].startswith("http"):
                element['slides'] = f"[:material-file-presentation-box: Slides]({element['slides']})"

        return append_to_page(markdown, list_of_dicts_to_md_table(data))

    elif path and re.compile(r"^checklists/SCSVS-\w*\.md$").match(path):
        # checklists.md
        column_titles = {'SCG ID': 'SCG ID', 'Platform': "Platform", 'Control / SCSTG Test': 'Control / SCSTG Test', 'L1': 'L1', 'L2': 'L2', 'R': 'R'}
        
        # Extract ID from path
        ID = re.compile(r"^checklists/(SCSVS-\w*)\.md$").match(path).group(1)
        print(f"Extracted ID: {ID}")  # Debugging line

        # Check if ID exists in CHECKLIST_DICT
        if ID not in CHECKLIST_DICT:
            print(f"Error: Checklist ID '{ID}' not found in CHECKLIST_DICT.")
            return markdown

        checklist = CHECKLIST_DICT[ID]
        print(f"Checklist found for ID '{ID}'.")  # Debugging line

        set_icons_for_web(checklist)

        cleaned_checklist = []
        for check in checklist:
            cleaned_check = dict(check)

            # Remove unwanted fields
            del cleaned_check['path']
            if 'SCSTG-TEST-ID' in cleaned_check:
                del cleaned_check['SCSTG-TEST-ID']
            cleaned_checklist.append(cleaned_check)

        # Dynamically set column_align based on the number of columns
        column_align = ["left"] * len(cleaned_checklist[0])

        # Convert to markdown table
        content = list_of_dicts_to_md_table(cleaned_checklist, column_titles, column_align) + "\n\n<br><br>"
        return append_to_page(markdown, content)

    return markdown
