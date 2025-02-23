from logger.logger import log, MOJA
import requests
import os


def getRefreshToken():
    return os.environ.get("RefreshToken")

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
        log.error(MOJA, f"Erreur lors de la requete GET a l'URL {url}: {response.status_code}")
        return None
    return response.json()

def sendPostRequest(url, data):
    response = requests.post(url, data=data)
    if response.status_code != 200:
        log.error(MOJA, f"Erreur lors de la requete POST a l'URL {url}: {response.status_code} ({response.json()})")
        return None
    return response.json()