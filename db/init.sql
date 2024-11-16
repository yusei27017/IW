CREATE TABLE lecturers (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL
);

CREATE TABLE courses (
    id INT AUTO_INCREMENT PRIMARY KEY,
    course_name VARCHAR(255) NOT NULL,
    description TEXT,
    start_time TIME NOT NULL,
    end_time TIME NOT NULL,
    lecturer_id INT NOT NULL,
    FOREIGN KEY (lecturer_id) REFERENCES lecturers(id)
);

INSERT INTO `mydatabase`.`lecturers` (`id`, `name`, `email`) VALUES 
('1', 'Alice Smith', 'alice.smith@example.com'),
('2', 'Bob Johnson', 'bob.johnson@example.com');

INSERT INTO `mydatabase`.`courses` (`course_name`, `description`, `start_time`, `end_time`, `lecturer_id`) VALUES
('Introduction to Python', 'Learn the basics of Python programming.', '09:00:00', '12:00:00', '1'),
('Advanced Python', 'Deep dive into advanced Python topics.', '13:00:00', '16:00:00', '1'),
('Introduction to SQL', 'Learn the fundamentals of SQL databases.', '10:00:00', '11:30:00', '2'),
('Data Analysis with SQL', 'Analyze data effectively using SQL.', '12:00:00', '14:30:00', '2');