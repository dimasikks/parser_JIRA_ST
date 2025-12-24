import requests
import json

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

def updateTasks(BASE_TOKEN, BASE_UUID, DOMAIN_ST, TABLE_NAME, issuesToUpdate, issues, COLUMNS_TO_FILL): # потенциально можно обьединить все в одну функцию с добавлением, но пока что оставлю так
    for issueToUpdate in issuesToUpdate:
        for issue in issues:
            issueName = issue['summary']

            if issueName == issueToUpdate["task_name"]:
                rowID = issueToUpdate["row_id"]

                payload = {
                    "updates": [
                        {
                        "row": {},
                        "row_id": rowID
                        }
                    ],
                    "table_name": TABLE_NAME
                }
                headers = {
                    "accept" : "application/json",
                    "authorization" : f"Bearer {BASE_TOKEN}"
                }
                url = f"{DOMAIN_ST}/api-gateway/api/v2/dtables/{BASE_UUID}/rows/"

                i = 0
                for key, value in issue.items():
                    payload["updates"][0]["row"][COLUMNS_TO_FILL[i]] = value
                    i+=1

                resultPayload = json.dumps(payload, indent=2)
  
                response = requests.put(url, headers=headers, data=resultPayload)

                if response.status_code == 200:
                    print(f"\nTask {issueName} successfully updated")
                else:
                    print(f"\nSomething went wrong: {response}")

                break

def addTasks(BASE_TOKEN, BASE_UUID, DOMAIN_ST, TABLE_NAME, issuesToAdd, issues, COLUMNS_TO_FILL): 
    for issueToAdd in issuesToAdd:
        for issue in issues:
            issueName = issue['summary']

            if issueName == issueToAdd:
                payload = {
                    "rows": [{}],
                    "table_name": TABLE_NAME,
                }
                headers = {
                    "accept" : "application/json",
                    "content-type": "application/json",
                    "authorization" : f"Bearer {BASE_TOKEN}"
                }
                url = f"{DOMAIN_ST}/api-gateway/api/v2/dtables/{BASE_UUID}/rows/"

                i = 0
                for key, value in issue.items():
                    payload["rows"][0][COLUMNS_TO_FILL[i]] = value
                    i+=1

                resultPayload = json.dumps(payload, indent=2)

                response = requests.post(url, headers=headers, data=resultPayload)

                if response.status_code == 200:
                    print(f"\nTask {issueName} successfully added")
                else:
                    print(f"\nSomething went wrong: {response}")
                
                break