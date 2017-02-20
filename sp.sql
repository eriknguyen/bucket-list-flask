
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
DELIMITER ;


-- stored procedure to add item to wish table
USE bucketlist;
DROP procedure IF EXISTS bucketlist.sp_addWish;

DELIMITER $$
USE bucketlist$$
CREATE DEFINER='root'@'localhost' PROCEDURE sp_addWish (
	IN p_title varchar(100),
	IN p_desc varchar(1000),
	IN p_user_id bigint)
BEGIN
insert into wish (title, `desc`, user_id, `date`)
	values (p_title, p_desc, p_user_id, NOW());
	END$$

	DELIMITER ;
	;


-- stored procedure to retrieve a wish from db
USE `bucketlist`;
DROP procedure IF EXISTS `sp_getWishByUser`;

DELIMITER $$
USE `bucketlist`$$
CREATE PROCEDURE `sp_getWishByUser` (
	IN p_user_id bigint
)
BEGIN
select * from wish where user_id = p_user_id;
END$$

DELIMITER ;


