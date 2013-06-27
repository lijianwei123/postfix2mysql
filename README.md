Python script that parses postfix maillog and stores it into MySQL/MariaDB table.

### Usage:

./postfix2mysql.py <log_file>

### Manual MySQL Table creation :

CREATE TABLE IF NOT EXISTS `log` (`id` INT NOT NULL AUTO_INCREMENT,`time` CHAR(60),`from` CHAR(60),`to`           CHAR(60), PRIMARY KEY (`id`));
