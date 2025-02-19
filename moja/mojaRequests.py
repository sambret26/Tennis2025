import requests
import os


def getRefreshToken():
    return "eyJhbGciOiJIUzUxMiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICIzYjQ2ODk1ZC0zN2EzLTQzM2QtYmQ1My01N2QxZTM1YTI3NzkifQ.eyJleHAiOjE3NDQ1NDM0NzksImlhdCI6MTczOTM1OTUyNCwianRpIjoiNTUxNjQyNzUtNGE4ZS00YjRjLTg1OTMtNmU5NDlkNmQ3MTVmIiwiaXNzIjoiaHR0cHM6Ly9hdXRoLmZmdC5mci9hdXRoL3JlYWxtcy9tYXN0ZXIiLCJhdWQiOiJodHRwczovL2F1dGguZmZ0LmZyL2F1dGgvcmVhbG1zL21hc3RlciIsInN1YiI6Ijg5NmM1MWUxLWVmMzQtNDIxYS1hMzM5LWJjMTQ5MWQ0ZjYwOCIsInR5cCI6IlJlZnJlc2giLCJhenAiOiJtb2phLXNpdGUiLCJzaWQiOiJhMTQwNzNmOS02Y2Y4LTQ5ZmQtYjM3OC05MTFiMzhlZjhhMTEiLCJzY29wZSI6InJvbGVzIHdyaXRlOnBhaWVtZW50IHdyaXRlOm1vamE6aG9tb2xvZ2F0aW9uIHJlYWQ6Y2xhc3NlbWVudCByZWFkOmlkZW50aXR5OmFsbCByZWFkOnBlcnNvbm5lIHNlYXJjaDppZGVudGl0eSByZWFkOmlkZW50aXR5OnVucHVibGlzaGVkIHByb2ZpbGUgd3JpdGU6ZmlsZXMgcmVhZDpsaWNlbmNlIG1vamE6cHJpdmUgY2xhc3NlbWVudF9yZWFkIGNsYXNzZW1lbnRfd3JpdGUgcmVhZDpjb21wZXRpdGlvbiByZWFkOnBhaWVtZW50IGVtYWlsIG1vamE6cHVibGljIn0.QhdqLknf6GbKh1KBOaTmppk9VWuzO2B5_IfQowcmSMeH5JOzMS06QaMTHOVakJPcCBRijc4OWw7X5d3pRIKzRQ"
def getAccessToken():
    url = os.environ.get("AccessTokenUrl")
    data = {
        "client_id": "moja-site",
        "client_secret": "d5a60529-5414-4e70-ae2c-56a182a39bb6",
        "refresh_token": getRefreshToken(),
        "grant_type": "refresh_token"
    }
    response = sendPostRequest(url, data)
    if response is None:
        return None
    return response["access_token"]

def createHeaders():
    return {"Authorization": "Bearer " + getAccessToken()}

def sendGetRequest(url):
    response =  requests.get(url, headers = createHeaders())
    if response.status_code != 200:
        print(f"Erreur lors de la requete GET a l'URL {url}: {response.status_code}")
        return None
    return response.json()

def sendPostRequest(url, data):
    response = requests.post(url, data=data)
    if response.status_code != 200:
        print(f"Erreur lors de la requete POST a l'URL {url}: {response.status_code} ({response.json()})")
        return None
    return response.json()