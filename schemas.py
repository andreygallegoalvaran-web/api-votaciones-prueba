from pydantic import BaseModel, EmailStr
from typing import Optional

class VoterBase(BaseModel):
    name: str
    email: EmailStr

class VoterCreate(VoterBase): pass

class Voter(VoterBase):
    id: int
    has_voted: bool
    class Config:
        from_attributes = True

class CandidateBase(BaseModel):
    name: str
    party: Optional[str] = None

class CandidateCreate(CandidateBase): pass

class Candidate(CandidateBase):
    id: int
    votes: int
    class Config:
        from_attributes = True

class VoteCreate(BaseModel):
    voter_id: int
    candidate_id: int

class Vote(BaseModel):
    id: int
    voter_id: int
    candidate_id: int
    class Config:
        from_attributes = True