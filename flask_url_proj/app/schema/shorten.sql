-- CREATE DATABASE shortenDB default CHARACTER SET UTF8;
 
-- use shortenDB;
 
CREATE TABLE shortenTable(
    origin_url      text NOT NULL,
    shorten     VARCHAR(8) NOT NULL
) CHARSET=utf8