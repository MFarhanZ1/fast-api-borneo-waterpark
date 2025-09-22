-- =================================================================
-- SKEMA DATABASE UNTUK CPANEL (MySQL / MariaDB)
-- Versi ini dijamin kompatibel dengan hosting cPanel.
-- =================================================================

-- -----------------------------------------------------------------
-- Tabel untuk menyimpan informasi harga tiket masuk
-- -----------------------------------------------------------------
CREATE TABLE `tiket_masuk` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `berlaku_untuk` ENUM('Weekend', 'Weekday', 'Anak_Anak_dibawah_80_cm') NOT NULL,
    `akronim` VARCHAR(15) NOT NULL,
    `harga` INT NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- -----------------------------------------------------------------
-- Tabel untuk menyimpan daftar barang yang bisa disewa
-- -----------------------------------------------------------------
CREATE TABLE `barang_disewakan` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `nama` VARCHAR(15) NOT NULL,
    `url_gambar` VARCHAR(255) NOT NULL,
    `akronim` VARCHAR(15) NOT NULL,
    `harga` INT NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- -----------------------------------------------------------------
-- Tabel untuk daftar fasilitas yang tersedia
-- -----------------------------------------------------------------
CREATE TABLE `fasilitas_tersedia` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `nama` VARCHAR(15) NOT NULL,
    `url_gambar` VARCHAR(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- -----------------------------------------------------------------
-- Tabel untuk menyimpan gambar dokumentasi dari customer
-- -----------------------------------------------------------------
CREATE TABLE `dokumentasi_cust` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `nama` VARCHAR(15) NOT NULL,
    `url_gambar` VARCHAR(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;