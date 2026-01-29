from sqlmodel import Field, SQLModel


class BaseApplicant(SQLModel):
    personal_name: str
    family_name: str


class ApplicantRecord(BaseApplicant, table=True):
    id: int | None = Field(default=None, primary_key=True)


class ApplicantView(BaseApplicant):
    id: int


class ApplicantUpdate(SQLModel):
    personal_name: str | None = None
    family_name: str | None = None
