CREATE TABLE GRADE
(ID         INTEGER PRIMARY KEY autoincrement,
 NAME       TEXT    NOT NULL,
 G_TIME     TEXT    NOT NULL,
 CDATE      datetime default (datetime('now', 'localtime')),
 EDATE      datetime default (datetime('now', 'localtime')) );