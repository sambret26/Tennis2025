from repositories.SettingRepository import SettingRepository
from logger.logger import log, MOJA
import requests
import time
import os

settingsRepository = SettingRepository()

def getRefreshToken():
    return settingsRepository.getRefreshToken()

def getClientSecret():
    return os.environ.get("ClientSecret")

def isTokenValid():
    return time.time() < float(os.environ.get("AccessTokenExpirationTime"))

def getAccessToken():
    accessToken = os.environ.get("AccessToken")
    if accessToken is not None :
        if isTokenValid():
            return accessToken
    url = os.environ.get("AccessTokenUrl")
    data = {
        "client_id": "moja-site",
        "client_secret": getClientSecret(),
        "refresh_token": getRefreshToken(),
        "grant_type": "refresh_token"
    }
    response = sendPostRequest(url, data)
    if response is None:
        return None
    accessToken = response["access_token"]
    expirationTime = response["expires_in"] - 30
    os.environ["AccessToken"] = accessToken
    os.environ["AccessTokenExpirationTime"] = str(time.time() + expirationTime)
    return accessToken

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