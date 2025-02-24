from models.Channel import Channel
from models.Category import Category
from database import db

class ChannelRepository:

    #GETTERS
    @staticmethod
    def getCategoryByChannelId(channelId):
        return db.session.query(Category).join(Channel, Category.code == Channel.category).filter(Channel.channelId == channelId).first()

    @staticmethod
    def getLogChannelId(category):
        return Channel.query.filter_by(category=category, type='Logs').first().channelId