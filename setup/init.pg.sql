-- -- CREATE TABLE for mindtickle_users
-- CREATE TABLE mindtickle_users (
--     user_id serial PRIMARY KEY,
--     user_name VARCHAR (255) NOT NULL,
--     active_status VARCHAR (10) NOT NULL
-- );

-- -- INSERT Sample Data
-- INSERT INTO mindtickle_users (user_id, user_name, active_status) VALUES
--     (1, 'User1', 'active'),
--     (2, 'User2', 'inactive'),
--     (3, 'User3', 'active'),
--     (4, 'User4', 'active');




-- CREATE TABLE for mindtickle_users
CREATE TABLE mindtickle_users (
    user_id serial PRIMARY KEY,
    user_name VARCHAR (255) NOT NULL,
    active_status VARCHAR (10) NOT NULL
);

-- INSERT Sample Data for mindtickle_users
INSERT INTO mindtickle_users (user_id, user_name, active_status) VALUES
    (1, 'User1', 'active'),
    (2, 'User2', 'inactive'),
    (3, 'User3', 'active'),
    (4, 'User4', 'active');

-- CREATE TABLE for lessons_completed
CREATE TABLE lessons_completed (
    id serial PRIMARY KEY,
    user_id INT NOT NULL,
    completion_date TIMESTAMP NOT NULL,
    FOREIGN KEY (user_id) REFERENCES mindtickle_users(user_id)
);

-- INSERT Sample Data for lessons_completed
INSERT INTO lessons_completed (user_id, completion_date) VALUES 
    (1, '2024-06-15 10:00:00'),
    (1, '2024-06-15 11:00:00'),
    (2, '2024-06-15 10:30:00'),
    (3, '2024-06-15 12:00:00'),
    (4, '2024-06-15 13:00:00');
