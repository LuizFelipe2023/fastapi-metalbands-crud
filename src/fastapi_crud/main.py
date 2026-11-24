from fastapi import Depends, FastAPI, HTTPException, Query, status
from scalar_fastapi import get_scalar_api_reference
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from fastapi.responses import RedirectResponse

from .database import Base, engine, get_db
from .models import BandDB
from .schemas import BandCreate, BandResponse, BandUpdate

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Metal Bands API",
    description="API CRUD para catálogo de bandas de Heavy Metal e subgêneros",
    version="1.0.0",
    docs_url=None,
)

@app.get("/", include_in_schema=False)
def root_redirect() -> RedirectResponse:
    return RedirectResponse(url="/docs", status_code=status.HTTP_307_TEMPORARY_REDIRECT)


@app.get("/docs", include_in_schema=False)
def scalar_docs():
    return get_scalar_api_reference(
        openapi_url=app.openapi_url,
        title=f"{app.title} - API Reference",
    )


def _get_band_or_404(band_id: int, db: Session) -> BandDB:
    band = db.get(BandDB, band_id)
    if not band:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Banda não encontrada",
        )
    return band


@app.post(
    "/bands",
    response_model=BandResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["Bands"],
    summary="Cadastrar banda",
)
def create_band(payload: BandCreate, db: Session = Depends(get_db)) -> BandDB:
    band = BandDB(**payload.model_dump())
    db.add(band)
    try:
        db.commit()
    except IntegrityError as exc:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"A banda '{payload.name}' já está cadastrada.",
        ) from exc
    db.refresh(band)
    return band


@app.get(
    "/bands",
    response_model=list[BandResponse],
    tags=["Bands"],
    summary="Listar bandas",
)
def list_bands(
    subgenre: str | None = Query(default=None, description="Filtrar por subgênero"),
    country: str | None = Query(default=None, description="Filtrar por país"),
    active: bool | None = Query(default=None, description="Filtrar bandas ativas ou encerradas"),
    db: Session = Depends(get_db),
) -> list[BandDB]:
    query = select(BandDB)

    if subgenre:
        query = query.where(BandDB.subgenre.ilike(f"%{subgenre}%"))
    if country:
        query = query.where(BandDB.country.ilike(f"%{country}%"))
    if active is not None:
        query = query.where(BandDB.active.is_(active))

    return list(db.scalars(query.order_by(BandDB.name)).all())


@app.get(
    "/bands/{band_id}",
    response_model=BandResponse,
    tags=["Bands"],
    summary="Buscar banda por ID",
)
def get_band(band_id: int, db: Session = Depends(get_db)) -> BandDB:
    return _get_band_or_404(band_id, db)


@app.patch(
    "/bands/{band_id}",
    response_model=BandResponse,
    tags=["Bands"],
    summary="Atualizar banda parcialmente",
)
def update_band(band_id: int, payload: BandUpdate, db: Session = Depends(get_db)) -> BandDB:
    band = _get_band_or_404(band_id, db)

    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(band, key, value)

    try:
        db.commit()
    except IntegrityError as exc:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Já existe outra banda com esse nome.",
        ) from exc
    db.refresh(band)
    return band


@app.delete(
    "/bands/{band_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    tags=["Bands"],
    summary="Remover banda",
)
def delete_band(band_id: int, db: Session = Depends(get_db)) -> None:
    band = _get_band_or_404(band_id, db)
    db.delete(band)
    db.commit()