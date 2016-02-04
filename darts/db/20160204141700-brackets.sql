
CREATE TABLE `brackets` (
	`id` INT(11) NULL AUTO_INCREMENT,
	`players` INT(11) NULL DEFAULT NULL,
	`bracketType` VARCHAR(255) NULL DEFAULT NULL,
	`createdAt` datetime DEFAULT NULL,
	PRIMARY KEY (`id`)
)
COLLATE='utf8_general_ci'
ENGINE=InnoDB;


CREATE TABLE `brackets_players` (
	`id` INT(11) NOT NULL AUTO_INCREMENT,
	`bracketId` INT(11) NULL DEFAULT NULL,
	`playerId` INT(11) NULL DEFAULT NULL,
	PRIMARY KEY (`id`),
	CONSTRAINT `fk_brackets_players_players` FOREIGN KEY (`playerId`) REFERENCES `players` (`id`),
	CONSTRAINT `fk_brackets_players_brackets` FOREIGN KEY (`bracketId`) REFERENCES `brackets` (`id`)
)
COLLATE='utf8_general_ci'
ENGINE=InnoDB;
