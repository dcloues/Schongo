CREATE TABLE chatter (
    id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    nick CHAR(9),
    channel VARCHAR(255) NOT NULL,
    chat_date DATETIME NOT NULL,
    chat VARCHAR(512) NOT NULL
) engine=XtraDB;
