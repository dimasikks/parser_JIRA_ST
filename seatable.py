import requests

def generateBaseToken(API_KEY_ST, EXP, DOMAIN_ST):
    headers = {
        "accept" : "application/json",
        "authorization" : f"Bearer {API_KEY_ST}"
    }
    url = f"{DOMAIN_ST}/api/v2.1/dtable/app-access-token/?exp={EXP}"

    response = requests.get(url, headers=headers).json()

    return [response['access_token'], response['dtable_uuid']]

def showBaseTokenAndBaseUUID(BASE_TOKEN, BASE_UUID):
    print(f"BASE_TOKEN: {BASE_TOKEN}\nBASE_UUID: {BASE_UUID}\n")

def getColumns(BASE_TOKEN, BASE_UUID, DOMAIN_ST, TABLE_NAME):
    headers = {
        "accept" : "application/json",
        "authorization" : f"Bearer {BASE_TOKEN}"
    }
    url = f"{DOMAIN_ST}/api-gateway/api/v2/dtables/{BASE_UUID}/columns/?table_name={TABLE_NAME}"

    response = requests.get(url, headers=headers).json()

    columns = []
    for column in response['columns']:
        columns.append(column['name'])

    return columns

def statusRows(BASE_TOKEN, BASE_UUID, DOMAIN_ST, TABLE_NAME, taskNames):
    headers = {
        "accept" : "application/json",
        "authorization" : f"Bearer {BASE_TOKEN}"
    }
    url = f"{DOMAIN_ST}/api-gateway/api/v2/dtables/{BASE_UUID}/rows/?table_name={TABLE_NAME}"

    response = requests.get(url, headers=headers).json()

    issuesToUpdate = []
    issuesToAdd = taskNames

    for row in response["rows"]:
        appendIssueStat = {}
        rowName = row["0000"]
        if rowName in taskNames:
            appendIssueStat["task_name"] = rowName
            appendIssueStat["row_id"] = row["_id"]

            issuesToUpdate.append(appendIssueStat)
            issuesToAdd.remove(rowName)

    return issuesToUpdate, issuesToAdd

def showResultOfStatusRows(issuesToUpdate, issuesToAdd):
    print(f"\nTheese tasks will be updated (task_name) - (row_id):")
    for issue in issuesToUpdate:
        print(f"""{issue["task_name"]} - {issue["row_id"]}""")

    print(f"\nTheese tasks will be added (task_name):")
    for issue in issuesToAdd:
        print(f"{issue}")

def updateTasks(issuesToUpdate, issues): # потенциально можно обьединить все в одну функцию с добавлением, но пока что оставлю так
    for issueToUpdate in issuesToUpdate:
        for issue in issues:
            issueName = issue['summary']

            if issueName == issueToUpdate["task_name"]:
                print(issueName)


