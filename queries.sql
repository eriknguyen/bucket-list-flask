
-- create a stored procedure to create a new user in user table
DELIMITER $$
CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_createUser`(
	IN p_name VARCHAR(50),
	IN p_email VARCHAR(50),
	IN p_password VARCHAR(200)
)
BEGIN
	if ( select exists (select 1 from user where email = p_email) ) THEN
		select 'Username Exists !!';
	ELSE
		insert into user(name, email, password) values (p_name, p_email, p_password);
	END IF;
END$$
DELIMITER ;

-- stored procedure to validate user
DELIMITER $$
CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_validateLogin` (
	IN p_email VARCHAR(50))
BEGIN
	select * from user where email = p_email;
END$$
DELIMITER;