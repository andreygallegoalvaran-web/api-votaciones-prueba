from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
import models, schemas
from database import engine, get_db

# Crear las tablas en la base de datos
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="API de Sistema de Votaciones",
    description="API RESTful para gestionar un sistema de votaciones, candidatos y estadísticas.",
    version="1.0.0"
)

# ==================== ENDPOINTS DE VOTANTES ====================

@app.post("/voters", response_model=schemas.Voter, status_code=status.HTTP_201_CREATED)
def create_voter(voter: schemas.VoterCreate, db: Session = Depends(get_db)):
    # Validación: El correo debe ser único
    db_voter = db.query(models.Voter).filter(models.Voter.email == voter.email).first()
    if db_voter:
        raise HTTPException(status_code=400, detail="Email ya registrado.")
    
    # Validación: Un votante no puede ser candidato (verificamos por nombre)
    is_candidate = db.query(models.Candidate).filter(models.Candidate.name == voter.name).first()
    if is_candidate:
        raise HTTPException(status_code=400, detail="Un candidato no puede registrarse como votante.")

    new_voter = models.Voter(name=voter.name, email=voter.email)
    db.add(new_voter)
    db.commit()
    db.refresh(new_voter)
    return new_voter

@app.get("/voters", response_model=List[schemas.Voter])
def get_voters(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(models.Voter).offset(skip).limit(limit).all()

@app.get("/voters/{voter_id}", response_model=schemas.Voter)
def get_voter(voter_id: int, db: Session = Depends(get_db)):
    voter = db.query(models.Voter).filter(models.Voter.id == voter_id).first()
    if not voter:
        raise HTTPException(status_code=404, detail="Votante no encontrado.")
    return voter

@app.delete("/voters/{voter_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_voter(voter_id: int, db: Session = Depends(get_db)):
    voter = db.query(models.Voter).filter(models.Voter.id == voter_id).first()
    if not voter:
        raise HTTPException(status_code=404, detail="Votante no encontrado.")
    db.delete(voter)
    db.commit()
    return None

# ==================== ENDPOINTS DE CANDIDATOS ====================

@app.post("/candidates", response_model=schemas.Candidate, status_code=status.HTTP_201_CREATED)
def create_candidate(candidate: schemas.CandidateCreate, db: Session = Depends(get_db)):
    # Validación: Nombre de candidato único
    db_candidate = db.query(models.Candidate).filter(models.Candidate.name == candidate.name).first()
    if db_candidate:
        raise HTTPException(status_code=400, detail="Candidato ya registrado.")
    
    # Validación: Un candidato no puede ser un votante existente
    is_voter = db.query(models.Voter).filter(models.Voter.name == candidate.name).first()
    if is_voter:
        raise HTTPException(status_code=400, detail="Un votante registrado no puede ser candidato.")

    new_candidate = models.Candidate(name=candidate.name, party=candidate.party)
    db.add(new_candidate)
    db.commit()
    db.refresh(new_candidate)
    return new_candidate

@app.get("/candidates", response_model=List[schemas.Candidate])
def get_candidates(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(models.Candidate).offset(skip).limit(limit).all()

@app.get("/candidates/{candidate_id}", response_model=schemas.Candidate)
def get_candidate(candidate_id: int, db: Session = Depends(get_db)):
    candidate = db.query(models.Candidate).filter(models.Candidate.id == candidate_id).first()
    if not candidate:
        raise HTTPException(status_code=404, detail="Candidato no encontrado.")
    return candidate

@app.delete("/candidates/{candidate_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_candidate(candidate_id: int, db: Session = Depends(get_db)):
    candidate = db.query(models.Candidate).filter(models.Candidate.id == candidate_id).first()
    if not candidate:
        raise HTTPException(status_code=404, detail="Candidato no encontrado.")
    db.delete(candidate)
    db.commit()
    return None

# ==================== ENDPOINTS DE VOTOS ====================

@app.post("/votes", response_model=schemas.Vote, status_code=status.HTTP_201_CREATED)
def cast_vote(vote: schemas.VoteCreate, db: Session = Depends(get_db)):
    voter = db.query(models.Voter).filter(models.Voter.id == vote.voter_id).first()
    candidate = db.query(models.Candidate).filter(models.Candidate.id == vote.candidate_id).first()

    # Validaciones
    if not voter:
        raise HTTPException(status_code=404, detail="Votante no encontrado.")
    if not candidate:
        raise HTTPException(status_code=404, detail="Candidato no encontrado.")
    if voter.has_voted:
        raise HTTPException(status_code=400, detail="El votante ya ha emitido su voto.")

    # Emitir el voto (Transacción)
    new_vote = models.Vote(voter_id=vote.voter_id, candidate_id=vote.candidate_id)
    voter.has_voted = True
    candidate.votes += 1

    db.add(new_vote)
    db.commit()
    db.refresh(new_vote)
    return new_vote

@app.get("/votes", response_model=List[schemas.Vote])
def get_votes(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(models.Vote).offset(skip).limit(limit).all()

@app.get("/votes/statistics")
def get_statistics(db: Session = Depends(get_db)):
    total_voters_voted = db.query(models.Voter).filter(models.Voter.has_voted == True).count()
    total_votes_cast = db.query(models.Vote).count()
    candidates = db.query(models.Candidate).all()

    statistics = {
        "total_voters_who_voted": total_voters_voted,
        "total_votes_system": total_votes_cast,
        "results": []
    }

    for candidate in candidates:
        percentage = (candidate.votes / total_votes_cast * 100) if total_votes_cast > 0 else 0
        statistics["results"].append({
            "candidate_id": candidate.id,
            "name": candidate.name,
            "party": candidate.party,
            "total_votes": candidate.votes,
            "percentage": f"{round(percentage, 2)}%"
        })

    # Ordenar por el que tiene más votos
    statistics["results"] = sorted(statistics["results"], key=lambda x: x["total_votes"], reverse=True)
    
    return statistics