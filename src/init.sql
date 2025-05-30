USE grades_db;

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

USE exams_db;

CREATE TABLE IF NOT EXISTS Exam (
    pruefungs_id INT AUTO_INCREMENT PRIMARY KEY,
    matrikelnummer INT NOT NULL,
    prof_name VARCHAR(255) NOT NULL,
    ects INT NOT NULL,
    datum DATE NOT NULL,
    modul VARCHAR(255) NOT NULL
);

INSERT INTO Exam (prof_name, ects, datum, modul) VALUES
('Prof. Müller', 5, '2024-07-01', 'Mathe'),
('Prof. Schmidt', 6, '2024-07-01', 'Physik'),
('Prof. Becker', 6, '2024-07-15', 'Informatik');