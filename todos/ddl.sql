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

CREATE TABLE user (
	id INTEGER NOT NULL AUTO_INCREMENT,
	username VARCHAR(256) NOT NULL,
	password VARCHAR(256) NOT NULL,
	PRIMARY KEY (id)
);

ALTER TABLE todo ADD COLUMN user_id INTEGER;
ALTER TABLE todo ADD FOREIGN KEY(user_id) REFERENCES user (id);
INSERT INTO user (username, password) VALUES ("admin", ”password”);
UPDATE todo SET user_id = 1 WHERE id = 1;
SELECT * FROM todo t JOIN user u ON t.user_id = u.id;