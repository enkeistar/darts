
RENAME TABLE `games` TO `matches`;

ALTER TABLE `teams`
	DROP FOREIGN KEY `fk_teams_games`;
ALTER TABLE `teams`
	CHANGE COLUMN `gameId` `matchId` INT(11) NULL DEFAULT NULL AFTER `id`;
ALTER TABLE `teams`
	ADD CONSTRAINT `fk_teams_matches` FOREIGN KEY (`matchId`) REFERENCES `matches` (`id`) ON UPDATE CASCADE ON DELETE CASCADE;


ALTER TABLE `marks`
	DROP FOREIGN KEY `fk_scores_games`;
ALTER TABLE `marks`
	CHANGE COLUMN `gameId` `matchId` INT(11) NULL DEFAULT NULL AFTER `id`;
ALTER TABLE `marks`
	ADD CONSTRAINT `fk_scores_matches` FOREIGN KEY (`matchId`) REFERENCES `matches` (`id`) ON UPDATE CASCADE ON DELETE CASCADE;


ALTER TABLE `results`
	DROP FOREIGN KEY `fk_results_games`;
ALTER TABLE `results`
	CHANGE COLUMN `gameId` `matchId` INT(11) NULL DEFAULT NULL AFTER `id`;
ALTER TABLE `results`
	ADD CONSTRAINT `fk_results_matches` FOREIGN KEY (`matchId`) REFERENCES `matches` (`id`) ON UPDATE CASCADE ON DELETE CASCADE;

ALTER TABLE `matches`
	ADD COLUMN `games` INT(11) NULL DEFAULT NULL AFTER `players`;

UPDATE `matches`
SET `games` = 3
WHERE `modeId` = 1;
