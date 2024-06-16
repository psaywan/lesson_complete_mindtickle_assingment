-- -- CREATE TABLE for lesson_completion
-- CREATE TABLE lesson_completion (
--     completion_id INT AUTO_INCREMENT PRIMARY KEY,
--     user_id INT NOT NULL,
--     lesson_id INT NOT NULL,
--     completion_date DATE NOT NULL
-- );

-- -- INSERT Sample Data
-- INSERT INTO lesson_completion (user_id, lesson_id, completion_date) VALUES
--     (1, 101, '2023-09-13'),
--     (2, 101, '2023-09-15'),
--     (3, 101, '2023-09-15'),
--     (4, 101, '2023-09-15'),
--     (1, 102, '2023-09-16'),
--     (2, 102, '2023-09-16'),
--     (3, 102, '2023-09-16'),
--     (4, 102, '2023-09-16'),
--     (1, 103, '2023-09-18'),
--     (2, 103, '2023-09-18'),
--     (3, 103, '2023-09-18'),
--     (4, 103, '2023-09-18'),
--     (1, 104, '2023-09-19'),
--     (2, 104, '2021-09-19'),
--     (3, 104, '2023-09-19'),
--     (4, 104, '2023-09-19'),
--     (1, 105, '2023-09-20'),
--     (2, 105, '2023-09-20'),
--     (3, 105, '2023-09-20'),
--     (4, 105, '2023-09-20'),
--     (1, 106, '2023-09-21'),
--     (2, 106, '2023-09-21'),
--     (3, 106, '2022-09-21'),
--     (4, 106, '2023-09-21'),
--     (1, 107, '2023-09-22'),
--     (2, 107, '2021-09-22'),
--     (3, 107, '2023-09-22'),
--     (4, 107, '2023-09-22');


-- Create the database
CREATE DATABASE IF NOT EXISTS mt_mysql;

-- Switch to the database
USE mt_mysql;

-- CREATE TABLE for users
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    active BOOLEAN NOT NULL DEFAULT TRUE
);

-- INSERT Sample Data for users
INSERT INTO users (name, active) VALUES ('User1', TRUE), ('User2', TRUE), ('User3', TRUE), ('User4', TRUE);

-- CREATE TABLE for lesson_completion
CREATE TABLE IF NOT EXISTS lesson_completion (
    completion_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    lesson_id INT NOT NULL,
    completion_date DATE NOT NULL
);

-- INSERT Sample Data for lesson_completion
INSERT INTO lesson_completion (user_id, lesson_id, completion_date) VALUES
    (1, 101, '2023-09-13'),
    (2, 101, '2023-09-15'),
    (3, 101, '2023-09-15'),
    (4, 101, '2023-09-15'),
    (1, 102, '2023-09-16'),
    (2, 102, '2023-09-16'),
    (3, 102, '2023-09-16'),
    (4, 102, '2023-09-16'),
    (1, 103, '2023-09-18'),
    (2, 103, '2023-09-18'),
    (3, 103, '2023-09-18'),
    (4, 103, '2023-09-18'),
    (1, 104, '2023-09-19'),
    (2, 104, '2021-09-19'),
    (3, 104, '2023-09-19'),
    (4, 104, '2023-09-19'),
    (1, 105, '2023-09-20'),
    (2, 105, '2023-09-20'),
    (3, 105, '2023-09-20'),
    (4, 105, '2023-09-20'),
    (1, 106, '2023-09-21'),
    (2, 106, '2023-09-21'),
    (3, 106, '2022-09-21'),
    (4, 106, '2023-09-21'),
    (1, 107, '2023-09-22'),
    (2, 107, '2021-09-22'),
    (3, 107, '2023-09-22'),
    (4, 107, '2023-09-22');

-- Drop existing user if exists
-- DROP USER IF EXISTS 'user'@'%';

-- Create a user and grant all privileges on all databases
-- CREATE USER 'user'@'%' IDENTIFIED BY 'user';
GRANT ALL PRIVILEGES ON *.* TO 'user'@'%';
FLUSH PRIVILEGES;