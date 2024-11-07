
from sqlalchemy import Column, Integer, SmallInteger, String, Float, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

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

    