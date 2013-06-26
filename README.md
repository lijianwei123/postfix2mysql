Python script that parses postfix maillog and stores it into MySQL/MariaDB table.

### Manual MySQL Table creation :

CREATE TABLE IF NOT EXISTS `log` ( 
    `id` INT NOT NULL AUTO_INCREMENT,
    `time` DATETIME NOT NULL,
    `from` CHAR(60) NOT NULL,
    `to` CHAR(60) NOT NULL,
     PRIMARY KEY (`id`));

