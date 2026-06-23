from sqlalchemy.orm import Session
import models
import schemas
from fastapi import HTTPException, status

# ==========================================
# LÓGICA PARA VOTANTES (VOTERS)
# ==========================================

def get_voter(db: Session, voter_id: int):
    return db.query(models.Voter).filter(models.Voter.id == voter_id).first()

def get_voter_by_email(db: Session, email: str):
    return db.query(models.Voter).filter(models.Voter.email == email).first()

def get_voters(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Voter).offset(skip).limit(limit).all()

def create_voter(db: Session, voter: schemas.VoterCreate):
    # Verificar que el nombre del votante no esté registrado como candidato
    candidate_exists = db.query(models.Candidate).filter(models.Candidate.name == voter.name).first()
    if candidate_exists:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Un candidato no puede ser registrado como votante."
        )

    # Verificar si el votante ya existe por email
    db_voter = get_voter_by_email(db, email=voter.email)
    if db_voter:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El correo electrónico ya se encuentra registrado."
        )

    db_voter = models.Voter(name=voter.name, email=voter.email)
    db.add(db_voter)
    db.commit()
    db.refresh(db_voter)
    return db_voter

def delete_voter(db: Session, voter_id: int):
    db_voter = get_voter(db, voter_id)
    if not db_voter:
        return None
    db.delete(db_voter)
    db.commit()
    return db_voter


# ==========================================
# LÓGICA PARA CANDIDATOS (CANDIDATES)
# ==========================================

def get_candidate(db: Session, candidate_id: int):
    return db.query(models.Candidate).filter(models.Candidate.id == candidate_id).first()

def get_candidates(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Candidate).offset(skip).limit(limit).all()

def create_candidate(db: Session, candidate: schemas.CandidateCreate):
    # Verificar que el candidato no exista previamente en la tabla de votantes
    voter_exists = db.query(models.Voter).filter(models.Voter.name == candidate.name).first()
    if voter_exists:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Un votante registrado no puede ser candidato."
        )

    db_candidate = models.Candidate(name=candidate.name, party=candidate.party)
    db.add(db_candidate)
    db.commit()
    db.refresh(db_candidate)
    return db_candidate

def delete_candidate(db: Session, candidate_id: int):
    db_candidate = get_candidate(db, candidate_id)
    if not db_candidate:
        return None
    db.delete(db_candidate)
    db.commit()
    return db_candidate


# ==========================================
# LÓGICA CRÍTICA: EMISIÓN DE VOTOS (VOTES)
# ==========================================

def create_vote(db: Session, vote: schemas.VoteCreate):
    # 1. Validar existencia e integridad del Votante
    db_voter = get_voter(db, vote.voter_id)
    if not db_voter:
        raise HTTPException(status_code=404, detail="El votante no existe.")
    
    if db_voter.has_voted:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="El votante ya ha emitido un voto previamente."
        )

    # 2. Validar existencia del Candidato
    db_candidate = get_candidate(db, vote.candidate_id)
    if not db_candidate:
        raise HTTPException(status_code=404, detail="El candidato seleccionado no existe.")

    try:
        # 3. PROCESO TRANSACCIONAL 
        db_vote = models.Vote(voter_id=vote.voter_id, candidate_id=vote.candidate_id)
        db.add(db_vote)

        # Actualizar estado del votante
        db_voter.has_voted = True

        # Incrementar conteo del candidato
        db_candidate.votes += 1

        db.commit()
        db.refresh(db_vote)
        return db_vote

    except Exception as e:
        db.rollback() 
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ocurrió un error interno al procesar el voto. Inténtelo de nuevo."
        )

def get_all_votes(db: Session):
    return db.query(models.Vote).all()


# ==========================================
# LÓGICA DE ESTADÍSTICAS (STATISTICS)
# ==========================================

def get_voting_statistics(db: Session):
    total_voted = db.query(models.Voter).filter(models.Voter.has_voted == True).count()
    candidates = db.query(models.Candidate).all()
    
    candidates_stats = []
    for c in candidates:
        percentage = (c.votes / total_voted * 100) if total_voted > 0 else 0.0
        
        candidates_stats.append({
            "id": c.id,
            "name": c.name,
            "party": c.party,
            "total_votes": c.votes,
            "percentage": f"{round(percentage, 2)}%" 
        })
        
    return {
        "total_voters_who_voted": total_voted,
        "total_votes_system": total_voted, # Agregado para coincidir con tu captura
        "results": candidates_stats
    }