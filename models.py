from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Voter(Base):
    __tablename__ = "voters"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    has_voted = Column(Boolean, default=False)
    votes = relationship("Vote", back_populates="voter")

class Candidate(Base):
    __tablename__ = "candidates"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    party = Column(String, nullable=True)
    votes = Column(Integer, default=0)
    votes_received = relationship("Vote", back_populates="candidate")

class Vote(Base):
    __tablename__ = "votes"
    id = Column(Integer, primary_key=True, index=True)
    voter_id = Column(Integer, ForeignKey("voters.id"))
    candidate_id = Column(Integer, ForeignKey("candidates.id"))
    voter = relationship("Voter", back_populates="votes")
    candidate = relationship("Candidate", back_populates="votes_received")