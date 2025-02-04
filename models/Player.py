from datetime import datetime
from models.PlayerAvailability import PlayerAvailability
from models.Payment import Payment

from database import db

class Player(db.Model):
    __tablename__ = "players"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    fftId = db.Column(db.String, unique=True, index=True)
    inscriptionId = db.Column(db.String, unique=True, index=True)
    lastName = db.Column(db.String, nullable=False)
    firstName = db.Column(db.String, nullable=False)
    rankingId = db.Column(db.Integer, db.ForeignKey("rankings.id"))
    club = db.Column(db.String)
    phoneNumber = db.Column(db.String)
    email = db.Column(db.String)
    isActive = db.Column(db.Boolean, default=True)
    createdAt = db.Column(db.DateTime, default=datetime.utcnow)
    updatedAt = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relations
    ranking = db.relationship('Ranking', foreign_keys=[rankingId], backref='players')
    # matches_as_player1 = relationship("Match", foreign_keys="[Match.player1_id]", back_populates="player1")
    # matches_as_player2 = relationship("Match", foreign_keys="[Match.player2_id]", back_populates="player2")
    # matches_won = relationship("Match", foreign_keys="[Match.winner_id]", back_populates="winner")
    categories = db.relationship("Category", 
                               secondary="player_categories",
                               backref=db.backref("players", lazy="dynamic"),
                               lazy="joined")
    payments = db.relationship("Payment", lazy="joined", back_populates="player")
    reductions = db.relationship("Reduction", backref="player", lazy="joined")
    balance = db.relationship("PlayerBalance", backref="player", uselist=False)

    def __init__(self, id=None, fftId=None, inscriptionId=None, lastName=None,
            firstName=None, rankingId=None, club=None, phoneNumber=None, email=None, isActive=None):
        self.id = id
        self.fftId = fftId
        self.inscriptionId = inscriptionId
        self.lastName = lastName
        self.firstName = firstName
        self.rankingId = rankingId
        self.club = club
        self.phoneNumber = phoneNumber
        self.email = email
        self.isActive = isActive

    def toDict(self):
        return {
            "id": self.id,
            "lastName": self.lastName,
            "firstName": self.firstName,
            "fftId": self.fftId,
            "inscriptionId": self.inscriptionId,
            "rankingId": self.rankingId,
            "club": self.club,
            "phoneNumber": self.phoneNumber,
            "email": self.email,
            "isActive": self.isActive,
            "ranking": self.ranking.toDict(),
            "categories": [category.code for category in self.categories],
            "balance": self.balance.toDictForPlayer(),
            "payments": [payment.toDictForPlayer() for payment in self.payments],
            "reductions": [reduction.toDictForPlayer() for reduction in self.reductions],
            "fullName": self.getFullName()
        }

    def toMiniDict(self):
        return {
            "fullName": self.getFullName(),
            "ranking": self.ranking.simple,
            "phoneNumber": self.phoneNumber,
            "email": self.email
        }

    def toNameDict(self):
        return {
            "id": self.id,
            "firstName": self.firstName,
            "lastName": self.lastName,
            "fullName": self.getFullName()
        }
    
    def getFullName(self):
        return f"{self.lastName.upper()} {self.firstName.title()}"

    @classmethod
    def fromJson(cls, data):
        return cls(
            fftId=data['fftId'],
            inscriptionId=data['inscriptionId'],        
            lastName=data['lastName'],        
            firstName=data['firstName'],        
            rankingId=data['rankingId'],        
            club=data['club'],        
            phoneNumber=data['phoneNumber'],
            email=data['email'],
            isActive=data['isActive']
        )
