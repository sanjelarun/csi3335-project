CREATE USER 'partyTimeUser'@'localhost' IDENTIFIED BY 'partyTimePassword';
GRANT ALL PRIVILEGES ON * . * TO 'partyTimeUser'@'localhost';
FLUSH PRIVILEGES;