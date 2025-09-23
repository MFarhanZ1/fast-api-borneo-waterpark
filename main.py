# =================================================================
# 1. IMPOR TETAP SAMA DENGAN VERSI SEBELUMNYA
# =================================================================
from fastapi import FastAPI, Depends, HTTPException, File, UploadFile, Form
from sqlalchemy.orm import Session
from typing import List, Optional # <-- TAMBAH Optional untuk PUT
import shutil
import uuid
import os # <-- TAMBAHKAN INI untuk menghapus file lama

import crud, models, schemas
from database import SessionLocal, engine, get_db
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

origins = [
    "*",
]

models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Borneo Waterpark API",
    description="API untuk mengelola data untuk Borneo Waterpark.",
    version="1.0.0"
)

app.mount("/static", StaticFiles(directory="static"), name="static")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =================================================================
# FUNGSI BANTU UNTUK MENYIMPAN GAMBAR (TIDAK BERUBAH)
# =================================================================
def save_upload_file(upload_file: UploadFile) -> str:
    """Menyimpan file yang di-upload dan mengembalikan URL publiknya."""
    unique_filename = f"{uuid.uuid4()}-{upload_file.filename}"
    file_location = f"static/images/{unique_filename}"
    
    with open(file_location, "wb+") as file_object:
        shutil.copyfileobj(upload_file.file, file_object)
        
    return f"/static/images/{unique_filename}"

# =================================================================
# FUNGSI BANTU UNTUK MENGHAPUS GAMBAR LAMA
# =================================================================
def delete_old_file(file_url: str):
    """Menghapus file dari disk berdasarkan URL-nya."""
    if file_url and "/static/images/" in file_url:
        # Ubah URL publik menjadi path fisik
        file_path = file_url.replace("/static/", "") # Menghapus /static/
        full_path = os.path.join("static", file_path) # Membuat path lengkap: static/images/namafile.jpg
        
        if os.path.exists(full_path):
            os.remove(full_path)
            print(f"File lama dihapus: {full_path}")
        else:
            print(f"File lama tidak ditemukan untuk dihapus: {full_path}")


# ===================================================================
# Endpoints untuk Tiket Masuk (TIDAK BERUBAH)
# ===================================================================
# ... (Kode endpoint Tiket Masuk Anda yang tidak berubah)
@app.post("/tiket/", response_model=schemas.Tiket, tags=["Tiket Masuk"])
def create_new_tiket(tiket: schemas.TiketCreate, db: Session = Depends(get_db)):
    return crud.create_tiket(db=db, tiket=tiket)

@app.get("/tiket/", response_model=List[schemas.Tiket], tags=["Tiket Masuk"])
def read_all_tiket(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_all_tiket(db, skip=skip, limit=limit)

@app.get("/tiket/{tiket_id}", response_model=schemas.Tiket, tags=["Tiket Masuk"])
def read_one_tiket(tiket_id: int, db: Session = Depends(get_db)):
    db_tiket = crud.get_tiket(db, tiket_id=tiket_id)
    if db_tiket is None:
        raise HTTPException(status_code=404, detail="Tiket tidak ditemukan")
    return db_tiket

@app.put("/tiket/{tiket_id}", response_model=schemas.Tiket, tags=["Tiket Masuk"])
def update_existing_tiket(tiket_id: int, tiket: schemas.TiketCreate, db: Session = Depends(get_db)):
    db_tiket = crud.update_tiket(db, tiket_id=tiket_id, tiket=tiket)
    if db_tiket is None:
        raise HTTPException(status_code=404, detail="Tiket tidak ditemukan")
    return db_tiket

@app.delete("/tiket/{tiket_id}", response_model=schemas.Tiket, tags=["Tiket Masuk"])
def delete_existing_tiket(tiket_id: int, db: Session = Depends(get_db)):
    db_tiket = crud.delete_tiket(db, tiket_id=tiket_id)
    if db_tiket is None:
        raise HTTPException(status_code=404, detail="Tiket tidak ditemukan")
    return db_tiket


# ===================================================================
# Endpoints untuk Barang Disewakan (POST & PUT DIUBAH)
# ===================================================================
@app.post("/barang/", response_model=schemas.Barang, tags=["Barang Disewakan"])
def create_new_barang(
    db: Session = Depends(get_db),
    nama: str = Form(...),
    akronim: str = Form(...),
    harga: int = Form(...),
    gambar: UploadFile = File(...)
):
    """Membuat data barang sewaan baru dengan upload gambar."""
    url_gambar_publik = save_upload_file(gambar)
    
    barang_data = schemas.BarangCreate(
        nama=nama,
        akronim=akronim,
        harga=harga,
        url_gambar=url_gambar_publik
    )
    return crud.create_barang(db=db, barang=barang_data)

@app.get("/barang/", response_model=List[schemas.Barang], tags=["Barang Disewakan"])
def read_all_barang(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_all_barang(db, skip=skip, limit=limit)

@app.get("/barang/{barang_id}", response_model=schemas.Barang, tags=["Barang Disewakan"])
def read_one_barang(barang_id: int, db: Session = Depends(get_db)):
    db_barang = crud.get_barang(db, barang_id=barang_id)
    if db_barang is None:
        raise HTTPException(status_code=404, detail="Barang tidak ditemukan")
    return db_barang

@app.put("/barang/{barang_id}", response_model=schemas.Barang, tags=["Barang Disewakan"])
async def update_existing_barang(
    barang_id: int,
    db: Session = Depends(get_db),
    nama: str = Form(...),
    akronim: str = Form(...),
    harga: int = Form(...),
    gambar: Optional[UploadFile] = File(None) # <-- OPSIONAL: User bisa tidak upload gambar baru
):
    """Memperbarui data barang sewaan berdasarkan ID, termasuk gambar."""
    db_barang = crud.get_barang(db, barang_id=barang_id)
    if db_barang is None:
        raise HTTPException(status_code=404, detail="Barang tidak ditemukan")

    url_gambar_publik = db_barang.url_gambar # Default: gunakan gambar yang sudah ada

    if gambar: # Jika ada gambar baru di-upload
        delete_old_file(db_barang.url_gambar) # Hapus gambar lama
        url_gambar_publik = save_upload_file(gambar) # Simpan gambar baru

    barang_data_update = schemas.BarangCreate( # schemas.BarangCreate masih bisa digunakan
        nama=nama,
        akronim=akronim,
        harga=harga,
        url_gambar=url_gambar_publik
    )
    return crud.update_barang(db, barang_id=barang_id, barang=barang_data_update)

@app.delete("/barang/{barang_id}", response_model=schemas.Barang, tags=["Barang Disewakan"])
def delete_existing_barang(barang_id: int, db: Session = Depends(get_db)):
    """Menghapus data barang sewaan berdasarkan ID."""
    db_barang = crud.delete_barang(db, barang_id=barang_id)
    if db_barang is None:
        raise HTTPException(status_code=404, detail="Barang tidak ditemukan")
    
    # Hapus juga file gambar dari disk saat data dihapus
    delete_old_file(db_barang.url_gambar)
    return db_barang


# ===================================================================
# Endpoints untuk Fasilitas Tersedia (POST & PUT DIUBAH)
# ===================================================================
@app.post("/fasilitas/", response_model=schemas.Fasilitas, tags=["Fasilitas Tersedia"])
def create_new_fasilitas(
    db: Session = Depends(get_db),
    nama: str = Form(...),
    gambar: UploadFile = File(...)
):
    """Membuat data fasilitas baru dengan upload gambar."""
    url_gambar_publik = save_upload_file(gambar)
    
    fasilitas_data = schemas.FasilitasCreate(
        nama=nama,
        url_gambar=url_gambar_publik
    )
    return crud.create_fasilitas(db=db, fasilitas=fasilitas_data)

@app.get("/fasilitas/", response_model=List[schemas.Fasilitas], tags=["Fasilitas Tersedia"])
def read_all_fasilitas(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_all_fasilitas(db, skip=skip, limit=limit)

@app.get("/fasilitas/{fasilitas_id}", response_model=schemas.Fasilitas, tags=["Fasilitas Tersedia"])
def read_one_fasilitas(fasilitas_id: int, db: Session = Depends(get_db)):
    db_fasilitas = crud.get_fasilitas(db, fasilitas_id=fasilitas_id)
    if db_fasilitas is None:
        raise HTTPException(status_code=404, detail="Fasilitas tidak ditemukan")
    return db_fasilitas

@app.put("/fasilitas/{fasilitas_id}", response_model=schemas.Fasilitas, tags=["Fasilitas Tersedia"])
async def update_existing_fasilitas(
    fasilitas_id: int,
    db: Session = Depends(get_db),
    nama: str = Form(...),
    gambar: Optional[UploadFile] = File(None)
):
    """Memperbarui data fasilitas berdasarkan ID, termasuk gambar."""
    db_fasilitas = crud.get_fasilitas(db, fasilitas_id=fasilitas_id)
    if db_fasilitas is None:
        raise HTTPException(status_code=404, detail="Fasilitas tidak ditemukan")

    url_gambar_publik = db_fasilitas.url_gambar

    if gambar:
        delete_old_file(db_fasilitas.url_gambar)
        url_gambar_publik = save_upload_file(gambar)

    fasilitas_data_update = schemas.FasilitasCreate(
        nama=nama,
        url_gambar=url_gambar_publik
    )
    return crud.update_fasilitas(db, fasilitas_id=fasilitas_id, fasilitas=fasilitas_data_update)

@app.delete("/fasilitas/{fasilitas_id}", response_model=schemas.Fasilitas, tags=["Fasilitas Tersedia"])
def delete_existing_fasilitas(fasilitas_id: int, db: Session = Depends(get_db)):
    """Menghapus data fasilitas berdasarkan ID."""
    db_fasilitas = crud.delete_fasilitas(db, fasilitas_id=fasilitas_id)
    if db_fasilitas is None:
        raise HTTPException(status_code=404, detail="Fasilitas tidak ditemukan")
    delete_old_file(db_fasilitas.url_gambar)
    return db_fasilitas


# ===================================================================
# Endpoints untuk Dokumentasi Customer (POST & PUT DIUBAH)
# ===================================================================
@app.post("/dokumentasi/", response_model=schemas.Dokumentasi, tags=["Dokumentasi Customer"])
def create_new_dokumentasi(
    db: Session = Depends(get_db),
    nama: str = Form(...),
    gambar: UploadFile = File(...)
):
    """Membuat data dokumentasi baru dengan upload gambar."""
    url_gambar_publik = save_upload_file(gambar)
    
    dokumentasi_data = schemas.DokumentasiCreate(
        nama=nama,
        url_gambar=url_gambar_publik
    )
    return crud.create_dokumentasi(db=db, dokumentasi=dokumentasi_data)

@app.get("/dokumentasi/", response_model=List[schemas.Dokumentasi], tags=["Dokumentasi Customer"])
def read_all_dokumentasi(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_all_dokumentasi(db, skip=skip, limit=limit)

@app.get("/dokumentasi/{dokumentasi_id}", response_model=schemas.Dokumentasi, tags=["Dokumentasi Customer"])
def read_one_dokumentasi(dokumentasi_id: int, db: Session = Depends(get_db)):
    db_dokumentasi = crud.get_dokumentasi(db, dokumentasi_id=dokumentasi_id)
    if db_dokumentasi is None:
        raise HTTPException(status_code=404, detail="Dokumentasi tidak ditemukan")
    return db_dokumentasi

@app.put("/dokumentasi/{dokumentasi_id}", response_model=schemas.Dokumentasi, tags=["Dokumentasi Customer"])
async def update_existing_dokumentasi(
    dokumentasi_id: int,
    db: Session = Depends(get_db),
    nama: str = Form(...),
    gambar: Optional[UploadFile] = File(None)
):
    """Memperbarui data dokumentasi berdasarkan ID, termasuk gambar."""
    db_dokumentasi = crud.get_dokumentasi(db, dokumentasi_id=dokumentasi_id)
    if db_dokumentasi is None:
        raise HTTPException(status_code=404, detail="Dokumentasi tidak ditemukan")

    url_gambar_publik = db_dokumentasi.url_gambar

    if gambar:
        delete_old_file(db_dokumentasi.url_gambar)
        url_gambar_publik = save_upload_file(gambar)

    dokumentasi_data_update = schemas.DokumentasiCreate(
        nama=nama,
        url_gambar=url_gambar_publik
    )
    return crud.update_dokumentasi(db, dokumentasi_id=dokumentasi_id, dokumentasi=dokumentasi_data_update)

@app.delete("/dokumentasi/{dokumentasi_id}", response_model=schemas.Dokumentasi, tags=["Dokumentasi Customer"])
def delete_existing_dokumentasi(dokumentasi_id: int, db: Session = Depends(get_db)):
    """Menghapus data dokumentasi berdasarkan ID."""
    db_dokumentasi = crud.delete_dokumentasi(db, dokumentasi_id=dokumentasi_id)
    if db_dokumentasi is None:
        raise HTTPException(status_code=404, detail="Dokumentasi tidak ditemukan")
    delete_old_file(db_dokumentasi.url_gambar)
    return db_dokumentasi