from sqlmodel import Field, SQLModel


class BaseExercise(SQLModel):
    minimum_grade: int
    maximum_grade: int


class ExerciseRecord(BaseExercise, table=True):
    id: int | None = Field(default=None, primary_key=True)


class ExerciseView(BaseExercise):
    id: int


class ExerciseUpdate(SQLModel):
    minimum_grade: int | None = None
    maximum_grade: int | None = None
