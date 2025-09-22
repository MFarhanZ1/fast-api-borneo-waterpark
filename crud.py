from sqlalchemy.orm import Session
import models, schemas

# === CRUD untuk Tiket Masuk ===

def get_tiket(db: Session, tiket_id: int):
    return db.query(models.TiketMasuk).filter(models.TiketMasuk.id == tiket_id).first()

def get_all_tiket(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.TiketMasuk).offset(skip).limit(limit).all()

def create_tiket(db: Session, tiket: schemas.TiketCreate):
    db_tiket = models.TiketMasuk(**tiket.dict())
    db.add(db_tiket)
    db.commit()
    db.refresh(db_tiket)
    return db_tiket

def update_tiket(db: Session, tiket_id: int, tiket: schemas.TiketCreate):
    db_tiket = get_tiket(db, tiket_id)
    if db_tiket:
        # Update field satu per satu
        db_tiket.berlaku_untuk = tiket.berlaku_untuk
        db_tiket.akronim = tiket.akronim
        db_tiket.harga = tiket.harga
        db.commit()
        db.refresh(db_tiket)
    return db_tiket

def delete_tiket(db: Session, tiket_id: int):
    db_tiket = get_tiket(db, tiket_id)
    if db_tiket:
        db.delete(db_tiket)
        db.commit()
    return db_tiket

# === CRUD untuk Barang Disewakan ===

def get_barang(db: Session, barang_id: int):
    return db.query(models.BarangDisewakan).filter(models.BarangDisewakan.id == barang_id).first()

def get_all_barang(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.BarangDisewakan).offset(skip).limit(limit).all()

def create_barang(db: Session, barang: schemas.BarangCreate):
    db_barang = models.BarangDisewakan(**barang.dict())
    db.add(db_barang)
    db.commit()
    db.refresh(db_barang)
    return db_barang
    
def update_barang(db: Session, barang_id: int, barang: schemas.BarangCreate):
    db_barang = get_barang(db, barang_id)
    if db_barang:
        db_barang.nama = barang.nama
        db_barang.url_gambar = barang.url_gambar
        db_barang.akronim = barang.akronim
        db_barang.harga = barang.harga
        db.commit()
        db.refresh(db_barang)
    return db_barang

def delete_barang(db: Session, barang_id: int):
    db_barang = get_barang(db, barang_id)
    if db_barang:
        db.delete(db_barang)
        db.commit()
    return db_barang

# === CRUD untuk Fasilitas Tersedia ===

def get_fasilitas(db: Session, fasilitas_id: int):
    return db.query(models.FasilitasTersedia).filter(models.FasilitasTersedia.id == fasilitas_id).first()

def get_all_fasilitas(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.FasilitasTersedia).offset(skip).limit(limit).all()

def create_fasilitas(db: Session, fasilitas: schemas.FasilitasCreate):
    db_fasilitas = models.FasilitasTersedia(**fasilitas.dict())
    db.add(db_fasilitas)
    db.commit()
    db.refresh(db_fasilitas)
    return db_fasilitas

def update_fasilitas(db: Session, fasilitas_id: int, fasilitas: schemas.FasilitasCreate):
    db_fasilitas = get_fasilitas(db, fasilitas_id)
    if db_fasilitas:
        db_fasilitas.nama = fasilitas.nama
        db_fasilitas.url_gambar = fasilitas.url_gambar
        db.commit()
        db.refresh(db_fasilitas)
    return db_fasilitas

def delete_fasilitas(db: Session, fasilitas_id: int):
    db_fasilitas = get_fasilitas(db, fasilitas_id)
    if db_fasilitas:
        db.delete(db_fasilitas)
        db.commit()
    return db_fasilitas

# === CRUD untuk Dokumentasi Customer ===

def get_dokumentasi(db: Session, dokumentasi_id: int):
    return db.query(models.DokumentasiCust).filter(models.DokumentasiCust.id == dokumentasi_id).first()

def get_all_dokumentasi(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.DokumentasiCust).offset(skip).limit(limit).all()

def create_dokumentasi(db: Session, dokumentasi: schemas.DokumentasiCreate):
    db_dokumentasi = models.DokumentasiCust(**dokumentasi.dict())
    db.add(db_dokumentasi)
    db.commit()
    db.refresh(db_dokumentasi)
    return db_dokumentasi

def update_dokumentasi(db: Session, dokumentasi_id: int, dokumentasi: schemas.DokumentasiCreate):
    db_dokumentasi = get_dokumentasi(db, dokumentasi_id)
    if db_dokumentasi:
        db_dokumentasi.nama = dokumentasi.nama
        db_dokumentasi.url_gambar = dokumentasi.url_gambar
        db.commit()
        db.refresh(db_dokumentasi)
    return db_dokumentasi

def delete_dokumentasi(db: Session, dokumentasi_id: int):
    db_dokumentasi = get_dokumentasi(db, dokumentasi_id)
    if db_dokumentasi:
        db.delete(db_dokumentasi)
        db.commit()
    return db_dokumentasi