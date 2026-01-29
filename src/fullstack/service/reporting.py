from fastapi import APIRouter
from sqlmodel import col, func, select

from fullstack.db import SessionDep
from fullstack.domain.applicant import ApplicantRecord
from fullstack.domain.application import ApplicationRecord
from fullstack.domain.exercise import ExerciseRecord

reporting_router = APIRouter(prefix="/reports")


@reporting_router.get("/applicants")
def get_applicants_count(session: SessionDep) -> int:
    return session.exec(select(func.count(col(ApplicantRecord.id)))).one()


@reporting_router.get("/applications")
def get_applications_count(session: SessionDep) -> int:
    return session.exec(select(func.count(col(ApplicationRecord.id)))).one()


@reporting_router.get("/exercises")
def get_exercises_count(session: SessionDep) -> int:
    return session.exec(select(func.count(col(ExerciseRecord.id)))).one()
