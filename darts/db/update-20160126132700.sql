
ALTER TABLE `marks` ADD COLUMN `value` INT(11) NULL DEFAULT NULL AFTER `bullseye`;

UPDATE `marks` SET `value` = 25 WHERE `bullseye` = 1;
UPDATE `marks` SET `value` = 20 WHERE `twenty` = 1;
UPDATE `marks` SET `value` = 19 WHERE `nineteen` = 1;
UPDATE `marks` SET `value` = 18 WHERE `eighteen` = 1;
UPDATE `marks` SET `value` = 17 WHERE `seventeen` = 1;
UPDATE `marks` SET `value` = 16 WHERE `sixteen` = 1;
UPDATE `marks` SET `value` = 15 WHERE `fifteen` = 1;
UPDATE `marks` SET `value` = 0 WHERE `value` IS NULL;


ALTER TABLE `marks`
	DROP COLUMN `twenty`,
	DROP COLUMN `nineteen`,
	DROP COLUMN `eighteen`,
	DROP COLUMN `seventeen`,
	DROP COLUMN `sixteen`,
	DROP COLUMN `fifteen`,
	DROP COLUMN `bullseye`;

ALTER TABLE `modes`
	ADD COLUMN `alias` VARCHAR(255) NULL DEFAULT NULL AFTER `mode`;

UPDATE `modes`
	SET `alias` = `value`;

UPDATE `modes`
	SET `alias` = 'x01' WHERE `alias` IN ('901','701','501','301');
