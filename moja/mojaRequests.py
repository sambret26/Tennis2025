from repositories.SettingRepository import SettingRepository
from repositories.MessageRepository import MessageRepository
from repositories.UrlRepository import UrlRepository
from models.Message import Message
from logger.logger import log, MOJA
import requests
import time
import os

settingsRepository = SettingRepository()
messageRepository = MessageRepository()
urlRepository = UrlRepository()

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
    if settingsRepository.getAuthError():
        return 500
    url = urlRepository.getUrlByLabel("AccessToken")
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
    accessToken = getAccessToken()
    if accessToken == 500:
        return None
    if accessToken is None :
        log.error(MOJA, "Erreur lors de la récupération du token d'authentification")
        message = Message("ERROR", "Erreur lors de la récupération du token d'authentification")
        messageRepository.addMessage(message)
        settingsRepository.setAuthError("1")
        return None
    return {"Authorization": "Bearer " + accessToken}

def sendGetRequest(url):
    headers = createHeaders()
    if headers is None :
        return None
    response =  requests.get(url, headers = headers)
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