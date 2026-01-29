from collections.abc import Sequence

from fastapi import APIRouter, HTTPException, Query
from sqlmodel import select
from starlette import status

from fullstack.db import SessionDep
from fullstack.domain.application import (
    ApplicationRecord,
    ApplicationUpdate,
    ApplicationView,
    BaseApplication,
)

application_router = APIRouter(prefix="/applications")
_NOT_FOUND = "Application not found"


@application_router.post("", response_model=ApplicationView)
def create_application(
    application: BaseApplication, session: SessionDep
) -> ApplicationRecord:
    record = ApplicationRecord.model_validate(application)
    session.add(record)
    session.commit()
    session.refresh(record)
    return record


@application_router.get("/{id}", response_model=ApplicationView)
def read_application(id: int, session: SessionDep) -> ApplicationRecord:
    application = session.get(ApplicationRecord, id)
    if not application:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=_NOT_FOUND)
    return application


@application_router.get("", response_model=list[ApplicationView])
def read_applications(
    session: SessionDep,
    offset: int = 0,
    limit: int = Query(default=100, le=100),
    applicant_id: int | None = Query(default=None),
    exercise_id: int | None = Query(default=None),
) -> Sequence[ApplicationRecord]:
    applicant_filter = (
        True if applicant_id is None else ApplicationRecord.applicant == applicant_id
    )
    exercise_filter = (
        True if exercise_id is None else ApplicationRecord.exercise == exercise_id
    )
    return session.exec(
        select(ApplicationRecord)
        .where(applicant_filter, exercise_filter)
        .offset(offset)
        .limit(limit)
    ).all()


@application_router.patch("/{id}", response_model=ApplicationView)
def update_application(
    session: SessionDep, id: int, application: ApplicationUpdate
) -> ApplicationRecord:
    record = session.get(ApplicationRecord, id)
    if not record:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=_NOT_FOUND)
    record.sqlmodel_update(application.model_dump(exclude_unset=True))
    session.add(record)
    session.commit()
    session.refresh(record)
    return record


@application_router.delete("/{id}")
def delete_application(session: SessionDep, id: int) -> bool:
    record = session.get(ApplicationRecord, id)
    if not record:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=_NOT_FOUND)
    session.delete(record)
    session.commit()
    return True
