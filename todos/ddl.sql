SHOW databases;
USE todos;
CREATE TABLE todo(
    id INT NOT NULL AUTO_INCREMENT,
    contents VARCHAR(256) NOT NULL,
    is_done BOOLEAN NOT NULL,
    PRIMARY KEY (id)
);
INSERT INTO todo (contents, is_done) VALUES ("FastAPI Section 0", true);
INSERT INTO todo (contents, is_done) VALUES ("FastAPI Section 1", true);
INSERT INTO todo (contents, is_done) VALUES ("FastAPI Section 2", false);
SELECT * FROM todo;
