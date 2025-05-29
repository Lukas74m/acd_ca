USE microservice_db;

CREATE TABLE IF NOT EXISTS Note (
    id INT AUTO_INCREMENT PRIMARY KEY,
    pruefungs_id INT NOT NULL,
    datum DATE NOT NULL,
    modul VARCHAR(255) NOT NULL,
    note VARCHAR(5) NOT NULL
);

INSERT INTO Note (pruefungs_id, datum, modul, note) VALUES
(1, '2024-07-01', 'Mathe', '1.3'),
(2, '2024-07-01', 'Physik', '2.0'),
(3, '2024-07-15', 'Informatik', '1.0');