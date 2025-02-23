from models.Message import Message
from database import db

class MessageRepository:

    @staticmethod
    def addMessage(message):
        db.session.add(message)
        db.session.commit()

    @staticmethod
    def addMessages(messages):
        db.session.add_all(messages)
        db.session.commit()

    @staticmethod
    def getMessagesByCategory(category):
        return Message.query.filter(Message.category == category).all()

    @staticmethod
    def getAllMessages():
        return Message.query.all()

    @staticmethod
    def deleteMessagesByCategory(category):
        Message.query.filter(Message.category == category).delete()
        db.session.commit()

    @staticmethod
    def deleteMessagesByIds(messageIds):
        Message.query.filter(Message.id.in_(messageIds)).delete()
        db.session.commit()