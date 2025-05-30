USE enrollment_service_db;

CREATE TABLE IF NOT EXISTS Exam (
    pruefungs_id INT AUTO_INCREMENT PRIMARY KEY,
    matrikelnummer INT NOT NULL,
    prof_name VARCHAR(255) NOT NULL,
    ects INT NOT NULL,
    datum DATE NOT NULL,
    modul VARCHAR(255) NOT NULL
);

INSERT INTO Exam (matrikelnummer, prof_name, ects, datum, modul) VALUES
(123456, 'Prof. Müller', 5, '2024-07-01', 'Mathe'),
(234567, 'Prof. Schmidt', 6, '2024-07-01', 'Physik'),
(345678, 'Prof. Becker', 6, '2024-07-15', 'Informatik');
