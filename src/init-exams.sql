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