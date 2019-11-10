create user 'newuser'@'localhost' IDENTIFIED BY 'password';
GRANT ALL privileges on * . * TO 'newuser'@'localhost';
flush privileges;