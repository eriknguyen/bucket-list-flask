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

-- stored procedure to get wish by id and user_id
DELIMITER $$
CREATE DEFINER='root'@'localhost' PROCEDURE `sp_getWishById` (
	IN p_id bigint,
	IN p_user_id bigint
)
BEGIN
select * from wish where id=p_id and user_id=p_user_id;
END$$
DELIMITER ;

-- update wish Detail
DELIMITER $$
CREATE DEFINER='root'@'localhost' PROCEDURE sp_updateWish (
	IN p_id bigint,
	IN p_title varchar(50),
	IN p_desc varchar(1000),
	IN p_user_id bigint
)
BEGIN
update wish
	set title=p_title, `desc` = p_desc
	where id=p_id and user_id=p_user_id;
	END$$
	DELIMITER ;

-- delete an item
DELIMITER $$
USE `bucketlist`$$
CREATE PROCEDURE `sp_deleteWish` (
	IN p_id bigint,
	IN p_user_id bigint
)
BEGIN
delete from wish where id = p_id and user_id = p_user_id;
END$$

DELIMITER ;