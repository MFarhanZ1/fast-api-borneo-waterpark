from pydantic import BaseModel
from typing import List, Optional
from models import BerlakuUntukEnum # Import enum dari models

# === Skema untuk Tiket Masuk ===
class TiketBase(BaseModel):
    berlaku_untuk: BerlakuUntukEnum
    akronim: str
    harga: int

class TiketCreate(TiketBase):
    pass

class Tiket(TiketBase):
    id: int
    class Config:
        from_attributes = True

# === Skema untuk Barang Disewakan ===
class BarangBase(BaseModel):
    nama: str
    url_gambar: str
    akronim: str
    harga: int

class BarangCreate(BarangBase):
    pass

class Barang(BarangBase):
    id: int
    class Config:
        from_attributes = True

# === Skema untuk Fasilitas Tersedia ===
class FasilitasBase(BaseModel):
    nama: str
    url_gambar: str

class FasilitasCreate(FasilitasBase):
    pass

class Fasilitas(FasilitasBase):
    id: int
    class Config:
        from_attributes = True

# === Skema untuk Dokumentasi Customer ===
class DokumentasiBase(BaseModel):
    nama: str
    url_gambar: str

class DokumentasiCreate(DokumentasiBase):
    pass

class Dokumentasi(DokumentasiBase):
    id: int
    class Config:
        from_attributes = True