USE exams_db;

CREATE TABLE IF NOT EXISTS Exam (
    pruefungs_id INT AUTO_INCREMENT PRIMARY KEY,
    prof_name VARCHAR(255) NOT NULL,
    ects INT NOT NULL,
    datum DATE NOT NULL,
    modul VARCHAR(255) NOT NULL
);

INSERT INTO Exam (prof_name, ects, datum, modul) VALUES
('Prof. Müller', 5, '2024-07-01', 'Mathematik'),
('Prof. Schmidt', 6, '2024-08-01', 'Physik'),
('Prof. Becker', 6, '2024-07-15', 'Informatik');

CREATE TABLE IF NOT EXISTS TeilnehmerListe (
    TeilnehmerListe_id INT AUTO_INCREMENT PRIMARY KEY,
    pruefungs_id INT NOT NULL,
    matrikelnummer INT NOT NULL,
    FOREIGN KEY (pruefungs_id) REFERENCES Exam(pruefungs_id) ON DELETE CASCADE
);

INSERT INTO TeilnehmerListe (pruefungs_id, matrikelnummer) VALUES
(1, 1234567),
(1, 2234567), 
(1, 3234567),
(2, 4234567),
(2, 5234567),
(3, 6234567),
(3, 7234567);

CREATE TABLE IF NOT EXISTS NotenListe (
    NotenListe_id INT AUTO_INCREMENT PRIMARY KEY,
    pruefungs_id INT NOT NULL,
    note_id INT NOT NULL
);

INSERT INTO NotenListe (pruefungs_id, note_id) VALUES
(1, 1),
(1, 2), 
(1, 3),
(2, 4),
(2, 5),
(3, 6);