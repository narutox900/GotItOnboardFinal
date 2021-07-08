CREATE DATABASE catalog_dev;
-- Grant permission
GRANT ALL PRIVILEGES ON project.* TO 'mysql_client'@'%';

CREATE DATABASE catalog_test;
-- Grant permission
GRANT ALL PRIVILEGES ON test.* TO 'mysql_client'@'%';