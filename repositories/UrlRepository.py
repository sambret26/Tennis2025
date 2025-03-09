from models.Url import Url

class UrlRepository:

    #GETTERS
    @staticmethod
    def getUrlByLabel(label):
        url = Url.query.filter_by(label=label).first()
        if url is None: 
            return None
        return url.url