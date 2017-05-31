/*
 Navicat Premium Data Transfer

 Source Server         : Local MAMP
 Source Server Type    : MySQL
 Source Server Version : 50634
 Source Host           : localhost
 Source Database       : bucketlist

 Target Server Type    : MySQL
 Target Server Version : 50634
 File Encoding         : utf-8

 Date: 05/31/2017 08:26:16 AM
*/

SET NAMES utf8;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
--  Table structure for `user`
-- ----------------------------
DROP TABLE IF EXISTS `user`;
CREATE TABLE `user` (
  `id` int(10) NOT NULL AUTO_INCREMENT,
  `name` varchar(50) DEFAULT NULL,
  `email` varchar(50) NOT NULL,
  `password` varchar(200) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8;

-- ----------------------------
--  Records of `user`
-- ----------------------------
BEGIN;
INSERT INTO `user` VALUES ('1', 'Erik', 'erik@abc.com', 'pbkdf2:sha1:1000$TsoL3Dlx$ccbd755247d3e10a638282d510bbd9c933a151a0'), ('2', 'Trang', 'trang@abc.com', 'pbkdf2:sha1:1000$yO6NWbP4$e23567690c4eefbbaeb225650f044e6e1fd3706e'), ('4', 'Khanh', 'khanh1@abc.com', 'pbkdf2:sha1:1000$PZL1YtEi$8653e205a7cadac56fef744858ff60b439dbcd97'), ('5', 'Trang', 'trang@hehe.com', 'pbkdf2:sha1:1000$c6vAJ82P$d1157266ce72be8948c02a763fc41f7c6cb02252');
COMMIT;

-- ----------------------------
--  Table structure for `wish`
-- ----------------------------
DROP TABLE IF EXISTS `wish`;
CREATE TABLE `wish` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(45) DEFAULT NULL,
  `desc` varchar(5000) DEFAULT NULL,
  `user_id` int(11) DEFAULT NULL,
  `date` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=latin1;

-- ----------------------------
--  Records of `wish`
-- ----------------------------
BEGIN;
INSERT INTO `wish` VALUES ('3', 'Note nay cua trang', 'hello hom nay phai lam xong cai chap nay', '2', '2017-02-20 22:33:33'), ('5', 'thu lan cuoi nhe', 'hihi kshdfklsj ', '2', '2017-02-20 23:06:52'), ('6', 'This is a new item', 'Today I\'m gonna finish this one, or maybe not but I\'ll still be happy', '2', '2017-02-23 00:24:03'), ('7', 'Thu cai xuong dong', 'thu xuong dong ne\r\n\r\nthu xuong dong nua ne hihi\r\ntest nha', '2', '2017-02-23 00:44:09');
COMMIT;

-- ----------------------------
--  Procedure structure for `sp_addWish`
-- ----------------------------
DROP PROCEDURE IF EXISTS `sp_addWish`;
delimiter ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_addWish`(
	IN p_title varchar(100),
	IN p_desc varchar(1000),
	IN p_user_id bigint)
BEGIN
	insert into wish (title, `desc`, user_id, `date`)
		values (p_title, p_desc, p_user_id, NOW());
END
 ;;
delimiter ;

-- ----------------------------
--  Procedure structure for `sp_createUser`
-- ----------------------------
DROP PROCEDURE IF EXISTS `sp_createUser`;
delimiter ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_createUser`(
    IN p_name VARCHAR(50),
    IN p_email VARCHAR(50),
    IN p_password VARCHAR(200)
)
BEGIN
    if ( select exists (select 1 from user where email = p_email) ) THEN
     
        select 'Username Exists !!';
     
    ELSE
     
        insert into user
        (
            name,
            email,
            password
        )
        values
        (
            p_name,
            p_email,
            p_password
        );
     
    END IF;
END
 ;;
delimiter ;

-- ----------------------------
--  Procedure structure for `sp_deleteWish`
-- ----------------------------
DROP PROCEDURE IF EXISTS `sp_deleteWish`;
delimiter ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_deleteWish`(
	IN p_id bigint,
	IN p_user_id bigint
)
BEGIN
delete from wish where id = p_id and user_id = p_user_id;
END
 ;;
delimiter ;

-- ----------------------------
--  Procedure structure for `sp_getWishById`
-- ----------------------------
DROP PROCEDURE IF EXISTS `sp_getWishById`;
delimiter ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_getWishById`(
	IN p_id bigint,
	IN p_user_id bigint
)
BEGIN
	select * from wish where id=p_id and user_id=p_user_id;
END
 ;;
delimiter ;

-- ----------------------------
--  Procedure structure for `sp_getWishByUser`
-- ----------------------------
DROP PROCEDURE IF EXISTS `sp_getWishByUser`;
delimiter ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_getWishByUser`(
IN p_user_id bigint,
IN p_limit int,
IN p_offset int,
out p_total bigint
)
BEGIN
     
    select count(*) into p_total from wish where user_id = p_user_id;
 
    SET @t1 = CONCAT( 'select * from wish where user_id = ', p_user_id, ' order by date desc limit ',p_limit,' offset ',p_offset);
    PREPARE stmt FROM @t1;
    EXECUTE stmt;
    DEALLOCATE PREPARE stmt;
END
 ;;
delimiter ;

-- ----------------------------
--  Procedure structure for `sp_updateWish`
-- ----------------------------
DROP PROCEDURE IF EXISTS `sp_updateWish`;
delimiter ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_updateWish`(
	IN p_id bigint,
	IN p_title varchar(50),
	IN p_desc varchar(1000),
	IN p_user_id bigint
)
BEGIN
	update wish
	set title=p_title, `desc` = p_desc
	where id=p_id and user_id=p_user_id;
END
 ;;
delimiter ;

-- ----------------------------
--  Procedure structure for `sp_validateLogin`
-- ----------------------------
DROP PROCEDURE IF EXISTS `sp_validateLogin`;
delimiter ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_validateLogin`(
	IN p_email VARCHAR(50))
BEGIN
	select * from user where email = p_email;
END
 ;;
delimiter ;

SET FOREIGN_KEY_CHECKS = 1;
