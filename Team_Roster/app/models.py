from sqlalchemy import CHAR, Column, Date, Double, Integer, SmallInteger, String, Float, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import db, login
import sqlalchemy as sa
import sqlalchemy.orm as so
from typing import Optional

Base = declarative_base()

class User(UserMixin,db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    username: so.Mapped[str] = so.mapped_column(sa.String(64),index=True,unique=True)
    email: so.Mapped[str] = so.mapped_column(sa.String(120),index=True,unique=True)
    password_hash: so.Mapped[Optional[str]] = so.mapped_column(sa.String(256))
    is_admin = db.Column(db.Boolean, default=False)
    is_active = db.Column(db.Boolean, default=True)

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

@login.user_loader
def load_user(id):
    return db.session.get(User, int(id))

class Team(Base):
    __tablename__ = 'teams'

    teams_ID = Column(Integer, primary_key=True, autoincrement=True)
    teamID = Column(String(3), nullable=False)
    yearID = Column(SmallInteger, nullable=False)
    lgID = Column(String(2), ForeignKey("leagues.lgID"), nullable=True)
    divID = Column(String(1), nullable=True)
    franchID = Column(String(3), ForeignKey("franchises.franchID"), nullable=True)
    team_name = Column(String(50), nullable=True)
    team_rank = Column(SmallInteger, nullable=True)
    team_G = Column(SmallInteger, nullable=True)
    team_G_home = Column(SmallInteger, nullable=True)
    team_W = Column(SmallInteger, nullable=True)
    team_L = Column(SmallInteger, nullable=True)
    DivWin = Column(String(1), nullable=True)
    WCWin = Column(String(1), nullable=True)
    LgWin = Column(String(1), nullable=True)
    WSWin = Column(String(1), nullable=True)
    team_R = Column(SmallInteger, nullable=True)
    team_AB = Column(SmallInteger, nullable=True)
    team_H = Column(SmallInteger, nullable=True)
    team_2B = Column(SmallInteger, nullable=True)
    team_3B = Column(SmallInteger, nullable=True)
    team_HR = Column(SmallInteger, nullable=True)
    team_BB = Column(SmallInteger, nullable=True)
    team_SO = Column(SmallInteger, nullable=True)
    team_SB = Column(SmallInteger, nullable=True)
    team_CS = Column(SmallInteger, nullable=True)
    team_HBP = Column(SmallInteger, nullable=True)
    team_SF = Column(SmallInteger, nullable=True)
    team_RA = Column(SmallInteger, nullable=True)
    team_ER = Column(SmallInteger, nullable=True)
    team_ERA = Column(Float, nullable=True)
    team_CG = Column(SmallInteger, nullable=True)
    team_SHO = Column(SmallInteger, nullable=True)
    team_SV = Column(SmallInteger, nullable=True)
    team_IPouts = Column(Integer, nullable=True)
    team_HA = Column(SmallInteger, nullable=True)
    team_HRA = Column(SmallInteger, nullable=True)
    team_BBA = Column(SmallInteger, nullable=True)
    team_SOA = Column(SmallInteger, nullable=True)
    team_E = Column(SmallInteger, nullable=True)
    team_DP = Column(SmallInteger, nullable=True)
    team_FP = Column(Float, nullable=True)
    park_name = Column(String(50), nullable=True)
    team_attendance = Column(Integer, nullable=True)
    team_BPF = Column(SmallInteger, nullable=True)
    team_PPF = Column(SmallInteger, nullable=True)
    team_projW = Column(SmallInteger, nullable=True)
    team_projL = Column(SmallInteger, nullable=True)

    def __repr__(self):
        return '<Team: {} {}, ID: {}>'.format(self.yearID,self.team_name,self.teamID)
    
class League(Base):
    __tablename__ = 'leagues'

    lgID = Column(String(2), primary_key=True)        
    league_name = Column(String(50), nullable=False)  
    league_active = Column(String(1), nullable=False) 

    def __repr__(self):
        return '<League: {}, ID:{}, Active: {}>'.format(self.league_name,self.lgID,self.league_active)
    
class Franchise(Base):
    __tablename__ = 'franchises'

    franchID = Column(String(3), primary_key=True) 
    franchName = Column(String(50), nullable=True) 
    active = Column(String(1), nullable=True)      
    NAassoc = Column(String(3), nullable=True)     

    def __repr__(self):
        return '<Franchise: {}, ID:{}, Active: {}>'.format(self.franchName,self.franchID,self.active)
    
class Fielding(Base):
    __tablename__ = 'fielding'
    
    fielding_ID = Column(Integer, primary_key=True, autoincrement=True)
    playerID = Column(String(9), nullable=False, index=True)
    yearID = Column(SmallInteger, nullable=False)
    teamID = Column(CHAR(3), nullable=False, index=True)
    stint = Column(SmallInteger, nullable=False)
    position = Column(String(2), nullable=True)
    f_G = Column(SmallInteger, nullable=True)
    f_GS = Column(SmallInteger, nullable=True)
    f_InnOuts = Column(SmallInteger, nullable=True)
    f_PO = Column(SmallInteger, nullable=True)
    f_A = Column(SmallInteger, nullable=True)
    f_E = Column(SmallInteger, nullable=True)
    f_DP = Column(SmallInteger, nullable=True)
    f_PB = Column(SmallInteger, nullable=True)
    f_WP = Column(SmallInteger, nullable=True)
    f_SB = Column(SmallInteger, nullable=True)
    f_CS = Column(SmallInteger, nullable=True)
    f_ZR = Column(Double, nullable=True)

    def __repr__(self):
        return '<Fielding: {} {}, TeamID:{}>'.format(self.yearID,self.fielding_ID,self.teamID)
    
class People(Base):
    __tablename__ = 'people'

    playerID = Column(String(9), primary_key=True, nullable=False)
    birthYear = Column(Integer, nullable=True)
    birthMonth = Column(Integer, nullable=True)
    birthDay = Column(Integer, nullable=True)
    birthCountry = Column(String(255), nullable=True)
    birthState = Column(String(255), nullable=True)
    birthCity = Column(String(255), nullable=True)
    deathYear = Column(Integer, nullable=True)
    deathMonth = Column(Integer, nullable=True)
    deathDay = Column(Integer, nullable=True)
    deathCountry = Column(String(255), nullable=True)
    deathState = Column(String(255), nullable=True)
    deathCity = Column(String(255), nullable=True)
    nameFirst = Column(String(255), nullable=True)
    nameLast = Column(String(255), nullable=True, index=True)
    nameGiven = Column(String(255), nullable=True)
    weight = Column(Integer, nullable=True)
    height = Column(Integer, nullable=True)
    bats = Column(String(255), nullable=True)
    throws = Column(String(255), nullable=True)
    debutDate = Column(Date, nullable=True)
    finalGameDate = Column(Date, nullable=True)

    def __repr__(self):
        return '<People: {} {}, ID:{}>'.format(self.nameFirst,self.nameLast,self.playerID)

class Batting(Base):

    __tablename__ = 'batting'

    batting_ID = Column(Integer, primary_key=True, autoincrement=True)
    playerID = Column(String(9), nullable=False, index=True)
    yearID = Column(SmallInteger, nullable=False)
    teamID = Column(CHAR(3), nullable=False, index=True)
    stint = Column(SmallInteger, nullable=False)
    b_G = Column(SmallInteger, nullable=True)
    b_AB = Column(SmallInteger, nullable=True)
    b_R = Column(SmallInteger, nullable=True)
    b_H = Column(SmallInteger, nullable=True)
    b_2B = Column(SmallInteger, nullable=True)
    b_3B = Column(SmallInteger, nullable=True)
    b_HR = Column(SmallInteger, nullable=True)
    b_RBI = Column(SmallInteger, nullable=True)
    b_SB = Column(SmallInteger, nullable=True)
    b_CS = Column(SmallInteger, nullable=True)
    b_BB = Column(SmallInteger, nullable=True)
    b_SO = Column(SmallInteger, nullable=True)
    b_IBB = Column(SmallInteger, nullable=True)
    b_HBP = Column(SmallInteger, nullable=True)
    b_SH = Column(SmallInteger, nullable=True)
    b_SF = Column(SmallInteger, nullable=True)
    b_GIDP = Column(SmallInteger, nullable=True)

    def __repr__(self):
        return '<Batting: {} {}, TeamID:{}>'.format(self.yearID, self.batting_ID, self.teamID)

class Pitching(Base):
    __tablename__ = 'pitching'

    pitching_ID = Column(Integer, primary_key=True, autoincrement=True)
    playerID = Column(String(9), ForeignKey("people.playerID"), nullable=False)
    yearID = Column(SmallInteger, nullable=False)
    teamID = Column(CHAR(3), nullable=False)
    stint = Column(SmallInteger, nullable=False)
    p_W = Column(SmallInteger, nullable=True)
    p_L = Column(SmallInteger, nullable=True)
    p_G = Column(SmallInteger, nullable=True)
    p_GS = Column(SmallInteger, nullable=True)
    p_CG = Column(SmallInteger, nullable=True)
    p_SHO = Column(SmallInteger, nullable=True)
    p_SV = Column(SmallInteger, nullable=True)
    p_IPOuts = Column(Integer, nullable=True)
    p_H = Column(SmallInteger, nullable=True)
    p_ER = Column(SmallInteger, nullable=True)
    p_HR = Column(SmallInteger, nullable=True)
    p_BB = Column(SmallInteger, nullable=True)
    p_SO = Column(SmallInteger, nullable=True)
    p_BAOpp = Column(Double, nullable=True)
    p_ERA = Column(Double, nullable=True)
    p_IBB = Column(SmallInteger, nullable=True)
    p_WP = Column(SmallInteger, nullable=True)
    p_HBP = Column(SmallInteger, nullable=True)
    p_BK = Column(SmallInteger, nullable=True)
    p_BFP = Column(SmallInteger, nullable=True)
    p_GF = Column(SmallInteger, nullable=True)
    p_R = Column(SmallInteger, nullable=True)
    p_SH = Column(SmallInteger, nullable=True)
    p_SF = Column(SmallInteger, nullable=True)
    p_GIDP = Column(SmallInteger, nullable=True)

    def __repr__(self):
        return (
            f"<Pitching(ID: {self.pitching_ID}, playerID: {self.playerID}, "
            f"yearID: {self.yearID}, teamID: {self.teamID}, stint: {self.stint})>"
        )

class Season(Base):
    __tablename__ = 'season'

    season_ID = Column(Integer, primary_key=True, autoincrement=True)
    yearID = Column(Integer, nullable=False)
    s_wOBA = Column(Double, nullable=True)
    s_wOBAScale = Column(Double, nullable=True)
    s_wBB = Column(Double, nullable=True)
    s_wHBP = Column(Double, nullable=True)
    s_w1B = Column(Double, nullable=True)
    s_w2B = Column(Double, nullable=True)
    s_w3B = Column(Double, nullable=True)
    s_wHR = Column(Double, nullable=True)
    s_runSB = Column(Double, nullable=True)
    s_runCS = Column(Double, nullable=True)
    s_R_PA = Column(Double, nullable=True)
    s_R_W = Column(Double, nullable=True)
    s_cFIP = Column(Double, nullable=True)

    def __repr__(self):
        return f"<Season {self.yearID})>"


class AllStarFull(Base):
    __tablename__ = 'allstarfull'

    allstarfull_ID = Column(Integer, primary_key=True, autoincrement=True)
    playerID = Column(String(9), ForeignKey("people.playerID"), nullable=False)
    lgID = Column(CHAR(2), ForeignKey("leagues.lgID"), nullable=False)
    teamID = Column(CHAR(3), nullable=False)
    yearID = Column(SmallInteger, nullable=False)
    gameID = Column(String(12), nullable=True)
    GP = Column(SmallInteger, nullable=True)
    startingPos = Column(SmallInteger, nullable=True)

    def __repr__(self):
        return (
            f"<AllStarFull(allstarfull_ID={self.allstarfull_ID}, playerID={self.playerID}, "
            f"yearID={self.yearID}, lgID={self.lgID}, teamID={self.teamID})>"
        )

class Awards(Base):
    __tablename__ = 'awards'

    awards_ID = Column(Integer, primary_key=True, autoincrement=True)
    awardID = Column(String(255), nullable=False)
    yearID = Column(SmallInteger, nullable=False)
    playerID = Column(String(9), ForeignKey("people.playerID"), nullable=False)
    lgID = Column(CHAR(2), ForeignKey("leagues.lgID"), nullable=False)
    tie = Column(String(1), nullable=True)
    notes = Column(String(100), nullable=True)

    def __repr__(self):
        return (
            f"<Awards(awards_ID={self.awards_ID}, awardID={self.awardID}, "
            f"yearID={self.yearID}, playerID={self.playerID}, lgID={self.lgID})>"
        )
