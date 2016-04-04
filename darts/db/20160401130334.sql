CREATE TABLE `mark_styles` (
	`id` INT NOT NULL AUTO_INCREMENT,
	`one` TEXT NULL DEFAULT NULL,
	`two` TEXT NULL DEFAULT NULL,
	`three` TEXT NULL DEFAULT NULL,
	`approved` TINYINT(1) DEFAULT NULL,
	PRIMARY KEY (`id`)
)
COLLATE='utf8_general_ci'
ENGINE=InnoDB;