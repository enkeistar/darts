CREATE TABLE `mark_styles` (
	`id` INT NOT NULL AUTO_INCREMENT,
	`one` LONGTEXT NULL DEFAULT NULL,
	`two` LONGTEXT NULL DEFAULT NULL,
	`three` LONGTEXT NULL DEFAULT NULL,
	`approved` TINYINT(1) DEFAULT NULL,
	PRIMARY KEY (`id`)
)
COLLATE='utf8_general_ci'
ENGINE=InnoDB;