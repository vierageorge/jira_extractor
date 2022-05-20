from jira import JIRA
from os import environ

#auth_jira = JIRA(token_auth='API token')

SERVER = 'https://msjira.morningstar.com'
INPUT_FILE = 'input'

def get_jira_api_key():
    api_key = environ.get('JIRA_API')
    if api_key is None:
        raise Exception("JIRA_API environment variable has not been set up.")
    return api_key

def create_jira_conn(server, api_key):
    return JIRA(server=server, token_auth=api_key)

def get_input_items(filepath):
    with open(filepath, 'r') as f:
        raw_rows=f.readlines()
    return [record.replace('\n','') for record in raw_rows]

def run():
    api_key = get_jira_api_key()
    jira = create_jira_conn(SERVER, api_key)
    issue_id_list = get_input_items(INPUT_FILE)
    for issue_id in issue_id_list:
        issue = jira.issue(issue_id, expand='changelog')
        changelog = issue.changelog
        for history in changelog.histories:
            for item in history.items:
                if item.field == 'status':
                    row = '	'.join([issue_id, history.created, history.author.name, item.fromString, item.toString])
                    print(row)

if __name__ == '__main__':
    run()