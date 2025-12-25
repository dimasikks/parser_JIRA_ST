import requests
import json

def takeTasks(API_KEY_JR, DOMAIN_JR, PROJECT_JR, FILTER_FIELD, FILTER_DATE_START, FIELDS_TO_TAKE, INCLUDE_FIELDS_TO_TAKE):
    headers = {
        "accept" : "application/json",
        "authorization" : f"Bearer {API_KEY_JR}"
    }
    url = f"{DOMAIN_JR}/rest/api/2/search?jql=project%20%3D%20{PROJECT_JR}%20AND%20cf%5B{FILTER_FIELD[0]}%5D%20%7E%20%22{FILTER_FIELD[1]}%22%20AND%20created%3E%22{FILTER_DATE_START}%22"

    response = requests.get(url, headers=headers).text
    finalJson = json.loads(response)

    issues = []
    fieldsToTake = FIELDS_TO_TAKE
    fieldsToTakeInclude = INCLUDE_FIELDS_TO_TAKE

    for issue in finalJson['issues']:
        issue_stat = {}

        for field in fieldsToTake:
            issue_stat[field] = issue['fields'][field]

        for fieldInclude in fieldsToTakeInclude:
            separatedFields = fieldInclude.split(".")

            result = issue['fields']
            for separatedField in separatedFields:
                result = result[separatedField]

            issue_stat[fieldInclude] = result

        issues.append(issue_stat)

    return issues

def takeTaskNames(issues):
    taskNames = []
    for issue in issues:
        taskNames.append(issue["summary"])

    return taskNames

def showTasks(issues):
    i = 0
    for issue in issues:
        i+=1
        print(f"""{issue["summary"]}""")
        for key, value in issue.items():
            print(f"{key}: {value}")
        print("\n")

def showTasksCount(issues):
    print(f"Received {len(issues)} tasks\n")
    