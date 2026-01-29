from sqlmodel import Field, SQLModel


class BaseApplication(SQLModel):
    applicant: int = Field(foreign_key="applicantrecord.id")
    exercise: int = Field(foreign_key="exerciserecord.id")


class ApplicationRecord(BaseApplication, table=True):
    id: int | None = Field(default=None, primary_key=True)


class ApplicationView(BaseApplication):
    id: int


class ApplicationUpdate(SQLModel):
    pass
