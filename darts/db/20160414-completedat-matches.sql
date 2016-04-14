
ALTER TABLE `matches`
	ADD COLUMN `completedAt` DATETIME NULL DEFAULT NULL AFTER `createdAt`;

UPDATE `matches`
SET `completedAt` = (
	SELECT `createdAt`
	FROM `marks`
	WHERE `matches`.`id` = `marks`.`matchId`
	ORDER BY `id` DESC
	LIMIT 1
)
WHERE `complete` = 1;
