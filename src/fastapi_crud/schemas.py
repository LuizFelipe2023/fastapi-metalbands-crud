from pydantic import BaseModel, ConfigDict, Field


class BandCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=120, examples=["Sepultura"])
    subgenre: str = Field(..., min_length=2, max_length=80, examples=["Thrash / Groove Metal"])
    country: str = Field(..., min_length=2, max_length=80, examples=["Brasil"])
    formed_year: int = Field(..., ge=1965, le=2026, examples=[1984])
    active: bool = True


class BandUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=120)
    subgenre: str | None = Field(default=None, min_length=2, max_length=80)
    country: str | None = Field(default=None, min_length=2, max_length=80)
    formed_year: int | None = Field(default=None, ge=1965, le=2026)
    active: bool | None = None


class BandResponse(BandCreate):
    model_config = ConfigDict(from_attributes=True)

    id: int