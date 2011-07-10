DROP TABLE IF EXISTS chatter;
CREATE TABLE chatter (
    id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    nick CHAR(9),
    channel VARCHAR(255) NOT NULL,
    chat_date DATETIME NOT NULL,
    chat VARCHAR(512) NOT NULL
) engine=XtraDB;

CREATE INDEX chatter_channel ON chatter (channel);
CREATE INDEX chatter_chat_date ON chatter (chat_date);

DROP TABLE IF EXISTS last_seen;
CREATE TABLE last_seen (
    nick CHAR(9) NOT NULL,
    channel VARCHAR(255) NOT NULL,
    last_seen DATETIME NOT NULL,
    PRIMARY KEY (nick, channel)
) engine=XtraDB;
