from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

import crud, models, schemas
from database import SessionLocal, engine, get_db

# Membuat tabel di database jika belum ada
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Borneo Waterpark API",
    description="API untuk mengelola data untuk Borneo Waterpark.",
    version="1.0.0"
)

# ===================================================================
# Endpoints untuk Tiket Masuk
# ===================================================================

@app.post("/tiket/", response_model=schemas.Tiket, tags=["Tiket Masuk"])
def create_new_tiket(tiket: schemas.TiketCreate, db: Session = Depends(get_db)):
    """Membuat data tiket baru."""
    return crud.create_tiket(db=db, tiket=tiket)

@app.get("/tiket/", response_model=List[schemas.Tiket], tags=["Tiket Masuk"])
def read_all_tiket(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Membaca semua data tiket."""
    return crud.get_all_tiket(db, skip=skip, limit=limit)

@app.get("/tiket/{tiket_id}", response_model=schemas.Tiket, tags=["Tiket Masuk"])
def read_one_tiket(tiket_id: int, db: Session = Depends(get_db)):
    """Membaca satu data tiket berdasarkan ID."""
    db_tiket = crud.get_tiket(db, tiket_id=tiket_id)
    if db_tiket is None:
        raise HTTPException(status_code=404, detail="Tiket tidak ditemukan")
    return db_tiket

@app.put("/tiket/{tiket_id}", response_model=schemas.Tiket, tags=["Tiket Masuk"])
def update_existing_tiket(tiket_id: int, tiket: schemas.TiketCreate, db: Session = Depends(get_db)):
    """Memperbarui data tiket berdasarkan ID."""
    db_tiket = crud.update_tiket(db, tiket_id=tiket_id, tiket=tiket)
    if db_tiket is None:
        raise HTTPException(status_code=404, detail="Tiket tidak ditemukan")
    return db_tiket

@app.delete("/tiket/{tiket_id}", response_model=schemas.Tiket, tags=["Tiket Masuk"])
def delete_existing_tiket(tiket_id: int, db: Session = Depends(get_db)):
    """Menghapus data tiket berdasarkan ID."""
    db_tiket = crud.delete_tiket(db, tiket_id=tiket_id)
    if db_tiket is None:
        raise HTTPException(status_code=404, detail="Tiket tidak ditemukan")
    return db_tiket

# ===================================================================
# Endpoints untuk Barang Disewakan
# ===================================================================

@app.post("/barang/", response_model=schemas.Barang, tags=["Barang Disewakan"])
def create_new_barang(barang: schemas.BarangCreate, db: Session = Depends(get_db)):
    """Membuat data barang sewaan baru."""
    return crud.create_barang(db=db, barang=barang)

@app.get("/barang/", response_model=List[schemas.Barang], tags=["Barang Disewakan"])
def read_all_barang(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Membaca semua data barang sewaan."""
    return crud.get_all_barang(db, skip=skip, limit=limit)

@app.get("/barang/{barang_id}", response_model=schemas.Barang, tags=["Barang Disewakan"])
def read_one_barang(barang_id: int, db: Session = Depends(get_db)):
    """Membaca satu data barang sewaan berdasarkan ID."""
    db_barang = crud.get_barang(db, barang_id=barang_id)
    if db_barang is None:
        raise HTTPException(status_code=404, detail="Barang tidak ditemukan")
    return db_barang

@app.put("/barang/{barang_id}", response_model=schemas.Barang, tags=["Barang Disewakan"])
def update_existing_barang(barang_id: int, barang: schemas.BarangCreate, db: Session = Depends(get_db)):
    """Memperbarui data barang sewaan berdasarkan ID."""
    db_barang = crud.update_barang(db, barang_id=barang_id, barang=barang)
    if db_barang is None:
        raise HTTPException(status_code=404, detail="Barang tidak ditemukan")
    return db_barang

@app.delete("/barang/{barang_id}", response_model=schemas.Barang, tags=["Barang Disewakan"])
def delete_existing_barang(barang_id: int, db: Session = Depends(get_db)):
    """Menghapus data barang sewaan berdasarkan ID."""
    db_barang = crud.delete_barang(db, barang_id=barang_id)
    if db_barang is None:
        raise HTTPException(status_code=404, detail="Barang tidak ditemukan")
    return db_barang

# ===================================================================
# Endpoints untuk Fasilitas Tersedia
# ===================================================================

@app.post("/fasilitas/", response_model=schemas.Fasilitas, tags=["Fasilitas Tersedia"])
def create_new_fasilitas(fasilitas: schemas.FasilitasCreate, db: Session = Depends(get_db)):
    """Membuat data fasilitas baru."""
    return crud.create_fasilitas(db=db, fasilitas=fasilitas)

@app.get("/fasilitas/", response_model=List[schemas.Fasilitas], tags=["Fasilitas Tersedia"])
def read_all_fasilitas(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Membaca semua data fasilitas."""
    return crud.get_all_fasilitas(db, skip=skip, limit=limit)

@app.get("/fasilitas/{fasilitas_id}", response_model=schemas.Fasilitas, tags=["Fasilitas Tersedia"])
def read_one_fasilitas(fasilitas_id: int, db: Session = Depends(get_db)):
    """Membaca satu data fasilitas berdasarkan ID."""
    db_fasilitas = crud.get_fasilitas(db, fasilitas_id=fasilitas_id)
    if db_fasilitas is None:
        raise HTTPException(status_code=404, detail="Fasilitas tidak ditemukan")
    return db_fasilitas

@app.put("/fasilitas/{fasilitas_id}", response_model=schemas.Fasilitas, tags=["Fasilitas Tersedia"])
def update_existing_fasilitas(fasilitas_id: int, fasilitas: schemas.FasilitasCreate, db: Session = Depends(get_db)):
    """Memperbarui data fasilitas berdasarkan ID."""
    db_fasilitas = crud.update_fasilitas(db, fasilitas_id=fasilitas_id, fasilitas=fasilitas)
    if db_fasilitas is None:
        raise HTTPException(status_code=404, detail="Fasilitas tidak ditemukan")
    return db_fasilitas

@app.delete("/fasilitas/{fasilitas_id}", response_model=schemas.Fasilitas, tags=["Fasilitas Tersedia"])
def delete_existing_fasilitas(fasilitas_id: int, db: Session = Depends(get_db)):
    """Menghapus data fasilitas berdasarkan ID."""
    db_fasilitas = crud.delete_fasilitas(db, fasilitas_id=fasilitas_id)
    if db_fasilitas is None:
        raise HTTPException(status_code=404, detail="Fasilitas tidak ditemukan")
    return db_fasilitas

# ===================================================================
# Endpoints untuk Dokumentasi Customer
# ===================================================================

@app.post("/dokumentasi/", response_model=schemas.Dokumentasi, tags=["Dokumentasi Customer"])
def create_new_dokumentasi(dokumentasi: schemas.DokumentasiCreate, db: Session = Depends(get_db)):
    """Membuat data dokumentasi baru."""
    return crud.create_dokumentasi(db=db, dokumentasi=dokumentasi)

@app.get("/dokumentasi/", response_model=List[schemas.Dokumentasi], tags=["Dokumentasi Customer"])
def read_all_dokumentasi(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Membaca semua data dokumentasi."""
    return crud.get_all_dokumentasi(db, skip=skip, limit=limit)

@app.get("/dokumentasi/{dokumentasi_id}", response_model=schemas.Dokumentasi, tags=["Dokumentasi Customer"])
def read_one_dokumentasi(dokumentasi_id: int, db: Session = Depends(get_db)):
    """Membaca satu data dokumentasi berdasarkan ID."""
    db_dokumentasi = crud.get_dokumentasi(db, dokumentasi_id=dokumentasi_id)
    if db_dokumentasi is None:
        raise HTTPException(status_code=404, detail="Dokumentasi tidak ditemukan")
    return db_dokumentasi

@app.put("/dokumentasi/{dokumentasi_id}", response_model=schemas.Dokumentasi, tags=["Dokumentasi Customer"])
def update_existing_dokumentasi(dokumentasi_id: int, dokumentasi: schemas.DokumentasiCreate, db: Session = Depends(get_db)):
    """Memperbarui data dokumentasi berdasarkan ID."""
    db_dokumentasi = crud.update_dokumentasi(db, dokumentasi_id=dokumentasi_id, dokumentasi=dokumentasi)
    if db_dokumentasi is None:
        raise HTTPException(status_code=404, detail="Dokumentasi tidak ditemukan")
    return db_dokumentasi

@app.delete("/dokumentasi/{dokumentasi_id}", response_model=schemas.Dokumentasi, tags=["Dokumentasi Customer"])
def delete_existing_dokumentasi(dokumentasi_id: int, db: Session = Depends(get_db)):
    """Menghapus data dokumentasi berdasarkan ID."""
    db_dokumentasi = crud.delete_dokumentasi(db, dokumentasi_id=dokumentasi_id)
    if db_dokumentasi is None:
        raise HTTPException(status_code=404, detail="Dokumentasi tidak ditemukan")
    return db_dokumentasi