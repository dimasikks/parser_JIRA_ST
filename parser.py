import jira
import seatable
import os

from dotenv import load_dotenv

load_dotenv()

#================# Jira #================#

API_KEY_JR = os.getenv("API_KEY_JR")
DOMAIN_JR = os.getenv("DOMAIN_JR")
PROJECT_JR = os.getenv("PROJECT_JR")
FIELDS_SEPARATOR = os.getenv("FIELDS_SEPARATOR")
FIELDS_TO_TAKE = os.getenv("FIELDS_TO_TAKE").split(FIELDS_SEPARATOR)
INCLUDE_FIELDS_TO_TAKE = os.getenv("INCLUDE_FIELDS_TO_TAKE").split(FIELDS_SEPARATOR)

issues = jira.takeTasks(API_KEY_JR, DOMAIN_JR, PROJECT_JR, FIELDS_TO_TAKE, INCLUDE_FIELDS_TO_TAKE)
taskNames = jira.takeTaskNames(issues)

jira.showTasks(issues)
jira.showTaskNames(taskNames)

#================# SeaTable #================#
API_KEY_ST = os.getenv("API_KEY_ST")
EXP = os.getenv("EXP")
DOMAIN_ST = os.getenv("DOMAIN_ST")
TABLE_NAME = os.getenv("TABLE_NAME")

BASE_TOKEN, BASE_UUID = seatable.generateBaseToken(API_KEY_ST, EXP, DOMAIN_ST)
seatable.showBaseTokenAndBaseUUID(BASE_TOKEN, BASE_UUID)

seatableColumns = seatable.getColumns(BASE_TOKEN, BASE_UUID, DOMAIN_ST, TABLE_NAME)

issuesToUpdate, issuesToAdd = seatable.statusRows(BASE_TOKEN, BASE_UUID, DOMAIN_ST, TABLE_NAME, taskNames)
seatable.showResultOfStatusRows(issuesToUpdate, issuesToAdd)

seatable.updateTasks(issuesToUpdate, issues)