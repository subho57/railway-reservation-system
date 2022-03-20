-- Adminer 4.8.1 MySQL 10.5.12-MariaDB dump

SET NAMES utf8;
SET time_zone = '+00:00';
SET foreign_key_checks = 0;
SET sql_mode = 'NO_AUTO_VALUE_ON_ZERO';

DROP TABLE IF EXISTS `station`;
CREATE TABLE `station` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `code` varchar(4) NOT NULL,
  `name` varchar(30) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=latin1;

INSERT INTO `station` (`id`, `code`, `name`) VALUES
(1,	'HWH',	'Howrah Juntion'),
(2,	'CGR',	'Chandan Nagar'),
(3,	'BNDL',	'Bandel Juntion'),
(4,	'HIND',	'Hindmotor'),
(5,	'NCR',	'Delhi - NCR');

DROP TABLE IF EXISTS `ticket`;
CREATE TABLE `ticket` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user` int(11) NOT NULL,
  `train` int(11) NOT NULL,
  `datetime` datetime NOT NULL,
  `seats` int(11) NOT NULL,
  `payment_mode` varchar(255) NOT NULL,
  `amount` decimal(10,2) NOT NULL,
  `booking_time` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `addon` tinyint(4) NOT NULL DEFAULT 0,
  PRIMARY KEY (`id`),
  KEY `user` (`user`),
  KEY `train` (`train`),
  CONSTRAINT `ticket_ibfk_3` FOREIGN KEY (`user`) REFERENCES `user` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `ticket_ibfk_4` FOREIGN KEY (`train`) REFERENCES `train` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=latin1;

INSERT INTO `ticket` (`id`, `user`, `train`, `datetime`, `seats`, `payment_mode`, `amount`, `booking_time`, `addon`) VALUES
(1,	8,	1,	'2022-03-20 07:54:00',	5,	'Cash',	150.00,	'2022-03-20 06:26:58',	0),
(2,	9,	3,	'2022-04-21 20:00:00',	4,	'UPI',	20840.00,	'2022-03-20 06:59:31',	1),
(3,	10,	3,	'2022-04-20 20:00:00',	5,	'cash',	24600.00,	'2022-03-20 07:02:19',	0);

DROP TABLE IF EXISTS `train`;
CREATE TABLE `train` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `source` int(11) NOT NULL,
  `destination` int(11) NOT NULL,
  `time` time NOT NULL,
  `fare` decimal(10,2) NOT NULL,
  `addon_type` varchar(255) NOT NULL,
  `addon_amount` decimal(10,2) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `source` (`source`),
  KEY `destination` (`destination`),
  CONSTRAINT `train_ibfk_1` FOREIGN KEY (`source`) REFERENCES `station` (`id`) ON DELETE CASCADE,
  CONSTRAINT `train_ibfk_2` FOREIGN KEY (`destination`) REFERENCES `station` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=latin1;

INSERT INTO `train` (`id`, `name`, `source`, `destination`, `time`, `fare`, `addon_type`, `addon_amount`) VALUES
(1,	'Howrah - Bandel Local',	1,	3,	'07:54:00',	30.00,	'NIL',	0.00),
(2,	'Howrah - Chandannagore Galloping',	1,	2,	'10:50:00',	40.00,	'NIL',	0.00),
(3,	'Rajdhani Express',	1,	5,	'20:00:00',	4920.00,	'Meals',	290.00);

DROP TABLE IF EXISTS `user`;
CREATE TABLE `user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=latin1;

INSERT INTO `user` (`id`, `name`) VALUES
(7,	'test'),
(8,	'Subhankar Pal'),
(9,	'Prerona Mazumder'),
(10,	'sam');

-- 2022-03-20 07:04:25
