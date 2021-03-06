from jira import JIRA
from os import environ

INPUT_FILE = 'input'
JIRA_KEY_ENV_VAR = 'JIRA_API'
JIRA_SERVER_ENV_VAR_NAME = 'JIRA_SERVER'

def get_jira_api_key():
    api_key = environ.get(JIRA_KEY_ENV_VAR)
    if api_key is None:
        raise Exception(f"{JIRA_KEY_ENV_VAR} environment variable has not been set up.")
    return api_key

def get_jira_server():
    jira_server = environ.get(JIRA_SERVER_ENV_VAR_NAME)
    if jira_server is None:
        raise Exception(f"{JIRA_SERVER_ENV_VAR_NAME} environment variable has not been set up.")
    return jira_server

def create_jira_conn(server, api_key):
    return JIRA(server=server, token_auth=api_key)

def get_input_items(filepath):
    with open(filepath, 'r') as f:
        raw_rows=f.readlines()
    return [record.strip(' \t\n') for record in raw_rows]

def get_issue_status_changelog(issue_id, jira_obj):
    result = []
    issue = jira_obj.issue(issue_id, expand='changelog')
    changelog = issue.changelog
    for history in changelog.histories:
        for item in history.items:
            if item.field == 'status':
                result.append([issue_id, history.created, history.author.name, item.fromString, item.toString])
    return result

def run():
    server = get_jira_server()
    api_key = get_jira_api_key()
    jira = create_jira_conn(server, api_key)
    issue_id_list = get_input_items(INPUT_FILE)
    history_list = []
    for issue_id in issue_id_list:
        history_list += get_issue_status_changelog(issue_id, jira)
    list(map(lambda record:print(*record, sep='\t'), history_list))

if __name__ == '__main__':
    run()