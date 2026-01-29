from collections.abc import Sequence

from fastapi import APIRouter, HTTPException, Query
from sqlmodel import select
from starlette import status

from fullstack.db import SessionDep
from fullstack.domain.applicant import (
    ApplicantRecord,
    ApplicantUpdate,
    ApplicantView,
    BaseApplicant,
)

applicant_router = APIRouter(prefix="/applicants")
_NOT_FOUND = "Applicant not found"


@applicant_router.post("", response_model=ApplicantView)
def create_applicant(applicant: BaseApplicant, session: SessionDep) -> ApplicantRecord:
    record = ApplicantRecord.model_validate(applicant)
    session.add(record)
    session.commit()
    session.refresh(record)
    return record


@applicant_router.get("/{id}", response_model=ApplicantView)
def read_applicant(id: int, session: SessionDep) -> ApplicantRecord:
    applicant = session.get(ApplicantRecord, id)
    if not applicant:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=_NOT_FOUND)
    return applicant


@applicant_router.get("", response_model=list[ApplicantView])
def read_applicants(
    session: SessionDep,
    offset: int = 0,
    limit: int = Query(default=100, le=100),
) -> Sequence[ApplicantRecord]:
    return session.exec(select(ApplicantRecord).offset(offset).limit(limit)).all()


@applicant_router.patch("/{id}", response_model=ApplicantView)
def update_applicant(
    session: SessionDep, id: int, applicant: ApplicantUpdate
) -> ApplicantRecord:
    record = session.get(ApplicantRecord, id)
    if not record:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=_NOT_FOUND)
    record.sqlmodel_update(applicant.model_dump(exclude_unset=True))
    session.add(record)
    session.commit()
    session.refresh(record)
    return record


@applicant_router.delete("/{id}")
def delete_applicant(session: SessionDep, id: int) -> bool:
    record = session.get(ApplicantRecord, id)
    if not record:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=_NOT_FOUND)
    session.delete(record)
    session.commit()
    return True
