CREATE DATABASE IF NOT EXISTS keuanganku;
USE keuanganku;

CREATE TABLE if NOT EXISTS accounts(
	user_id INT(11) NOT NULL AUTO_INCREMENT,
	username VARCHAR(50) NOT NULL,
	passwords VARCHAR(255) NOT NULL,
	email VARCHAR(100) NOT NULL,
	PRIMARY KEY (user_id)
);

CREATE TABLE if NOT EXISTS accounts_accounting(
	keuangan INT(11) NOT NULL AUTO_INCREMENT,
	tanggal DATE NOT NULL,
	rupiah VARCHAR(255) NOT NULL,
	jenis VARCHAR(100) NOT NULL,
	user_id INT(11) NOT NULL,
	FOREIGN KEY (user_id) REFERENCES accounts(user_id)
	PRIMARY KEY (keuangan)
);

CREATE TABLE if NOT EXISTS accounts_accounting_result(
	result_id INT(11) NOT NULL AUTO_INCREMENT,
	bulan VARCHAR(12) NOT NULL,
	rupiah INT(255) NOT NULL,
	user_id INT(11) NOT NULL,
	FOREIGN KEY (user_id) REFERENCES accounts(user_id),
	PRIMARY KEY (result_id)
);

