from gamelog import db
from datetime import datetime
from flask_login import UserMixin
from sqlalchemy.orm import relationship

players = db.Table("players", 
                    db.Column("id", db.Integer, db.ForeignKey("users.id")),
                    db.Column("winner_id", db.Integer, db.ForeignKey("heart_of_crown.winner_id"))
                   )

# Users
class Users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    player = db.relationship("Heart_of_crown", secondary=players, backref=db.backref("current_players", lazy="dynamic"))
    
    def __repr__(self):
        return "Users('{}', '{}')".format(self.username, self.date_created)
        
# Heart of Crown
class Heart_of_crown(db.Model):
    game_id = db.Column(db.Integer, primary_key=True)
    genre = db.Column(db.String(100))
    date_played = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    deck = db.Column(db.String(100), nullable=False, default="Random")
    sudden_death = db.Column(db.Boolean, nullable=False, default=False)
    winner_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    loser_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    winner_queen = db.Column(db.String(50), nullable=False)
    loser_queen = db.Column(db.String(50), nullable=True)
    winner_score = db.Column(db.Integer, nullable=False)
    loser_score = db.Column(db.Integer, nullable=False)
    
    winner = db.relationship("Users", foreign_keys=[winner_id])
    loser = db.relationship("Users", foreign_keys=[loser_id])
    
    def __repr__(self):
        return "Heart_of_crown('{}', '{}', '{}', '{}', '{}')".format(self.date_played, self.deck, self.winner_id, self.winner_queen, self.winner_score)

class Map(db.Model):
    id = db.Column(db.Integer, db.Sequence('map_seq'), primary_key=True)
    
        