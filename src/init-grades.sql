USE grades_db;

CREATE TABLE IF NOT EXISTS Note (
    note_id INT AUTO_INCREMENT PRIMARY KEY,
    pruefungs_id INT NOT NULL,
    datum DATE NOT NULL,
    modul VARCHAR(255) NOT NULL,
    note VARCHAR(5) NOT NULL
);

INSERT INTO Note (pruefungs_id, datum, modul, note) VALUES
(1, '2024-07-01', 'Mathematik', '1.3'),
(1, '2024-07-01', 'Mathematik', '2.0'),
(1, '2024-07-01', 'Mathematik', '1.7'),
(2, '2024-07-15', 'Informatik', '1.0'),
(2, '2024-07-15', 'Informatik', '2.3'),
(3, '2024-08-01', 'Physik', '1.7');

CREATE TABLE IF NOT EXISTS users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(100) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,  -- Klartext-Passwort
    role ENUM('student', 'professor') NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO users (username, email, password, role) VALUES
('prof.mueller', 'mueller@university.de', 'password123', 'professor'),
('student.max', 'max@student.de', 'password123', 'student'),
('student.anna', 'anna@student.de', 'password123', 'student');

CREATE TABLE IF NOT EXISTS NotenListe (
    NotenListe_id INT AUTO_INCREMENT PRIMARY KEY,
    pruefungs_id INT NOT NULL,
    note_id INT NOT NULL,
    FOREIGN KEY (note_id) REFERENCES Note(note_id) ON DELETE CASCADE
);

INSERT INTO NotenListe (pruefungs_id, note_id) VALUES
(1, 1),
(1, 2), 
(1, 3),
(2, 4),
(2, 5),
(3, 6);

