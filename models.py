from sqlalchemy import Column, Integer, String, Enum
from database import Base
import enum

class BerlakuUntukEnum(str, enum.Enum):
    Weekend = "Weekend"
    Weekday = "Weekday"
    Anak_Anak_dibawah_80_cm = "Anak_Anak_dibawah_80_cm"

class TiketMasuk(Base):
    __tablename__ = "tiket_masuk"
    id = Column(Integer, primary_key=True, index=True)
    berlaku_untuk = Column(Enum(BerlakuUntukEnum), nullable=False)
    akronim = Column(String(15), nullable=False)
    harga = Column(Integer, nullable=False)

class BarangDisewakan(Base):
    __tablename__ = "barang_disewakan"
    id = Column(Integer, primary_key=True, index=True)
    nama = Column(String(15), nullable=False)
    url_gambar = Column(String(255), nullable=False)
    akronim = Column(String(15), nullable=False)
    harga = Column(Integer, nullable=False)
    
class FasilitasTersedia(Base):
    __tablename__ = "fasilitas_tersedia"
    id = Column(Integer, primary_key=True, index=True)
    nama = Column(String(15), nullable=False)
    url_gambar = Column(String(255), nullable=False)

class DokumentasiCust(Base):
    __tablename__ = "dokumentasi_cust"
    id = Column(Integer, primary_key=True, index=True)
    nama = Column(String(15), nullable=False)
    url_gambar = Column(String(255), nullable=False)