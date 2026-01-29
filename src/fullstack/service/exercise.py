from collections.abc import Sequence

from fastapi import APIRouter, HTTPException, Query
from sqlmodel import select
from starlette import status

from fullstack.db import SessionDep
from fullstack.domain.exercise import (
    BaseExercise,
    ExerciseRecord,
    ExerciseUpdate,
    ExerciseView,
)

exercise_router = APIRouter(prefix="/exercises")
_NOT_FOUND = "Exercise not found"


@exercise_router.post("", response_model=ExerciseView)
def create_exercise(exercise: BaseExercise, session: SessionDep) -> ExerciseRecord:
    record = ExerciseRecord.model_validate(exercise)
    session.add(record)
    session.commit()
    session.refresh(record)
    return record


@exercise_router.get("/{id}", response_model=ExerciseView)
def read_exercise(id: int, session: SessionDep) -> ExerciseRecord:
    exercise = session.get(ExerciseRecord, id)
    if not exercise:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=_NOT_FOUND)
    return exercise


@exercise_router.get("", response_model=list[ExerciseView])
def read_exercises(
    session: SessionDep,
    offset: int = 0,
    limit: int = Query(default=100, le=100),
) -> Sequence[ExerciseRecord]:
    return session.exec(select(ExerciseRecord).offset(offset).limit(limit)).all()


@exercise_router.patch("/{id}", response_model=ExerciseView)
def update_exercise(
    session: SessionDep, id: int, exercise: ExerciseUpdate
) -> ExerciseRecord:
    record = session.get(ExerciseRecord, id)
    if not record:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=_NOT_FOUND)
    record.sqlmodel_update(exercise.model_dump(exclude_unset=True))
    session.add(record)
    session.commit()
    session.refresh(record)
    return record


@exercise_router.delete("/{id}")
def delete_exercise(session: SessionDep, id: int) -> bool:
    record = session.get(ExerciseRecord, id)
    if not record:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=_NOT_FOUND)
    session.delete(record)
    session.commit()
    return True
