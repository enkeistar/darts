CREATE TABLE IF NOT EXISTS `games` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `players` int(11) DEFAULT NULL,
  `game` int(11) DEFAULT NULL,
  `round` int(11) DEFAULT NULL,
  `ready` tinyint(4) DEFAULT NULL,
  `turn` int(11) DEFAULT NULL,
  `createdAt` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

CREATE TABLE IF NOT EXISTS `marks` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `gameId` int(11) DEFAULT NULL,
  `teamId` int(11) DEFAULT NULL,
  `playerId` int(11) DEFAULT NULL,
  `game` int(11) DEFAULT NULL,
  `round` int(11) DEFAULT NULL,
  `twenty` tinyint(4) DEFAULT NULL,
  `nineteen` tinyint(4) DEFAULT NULL,
  `eighteen` tinyint(4) DEFAULT NULL,
  `seventeen` tinyint(4) DEFAULT NULL,
  `sixteen` tinyint(4) DEFAULT NULL,
  `fifteen` tinyint(4) DEFAULT NULL,
  `bullseye` tinyint(4) DEFAULT NULL,
  `createdAt` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_scores_games` (`gameId`),
  KEY `fk_scores_teams` (`teamId`),
  KEY `fk_scores_players` (`playerId`),
  CONSTRAINT `fk_scores_games` FOREIGN KEY (`gameId`) REFERENCES `games` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `fk_scores_players` FOREIGN KEY (`playerId`) REFERENCES `players` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `fk_scores_teams` FOREIGN KEY (`teamId`) REFERENCES `teams` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

CREATE TABLE IF NOT EXISTS `players` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

CREATE TABLE IF NOT EXISTS `results` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `gameId` int(11) DEFAULT NULL,
  `teamId` int(11) DEFAULT NULL,
  `game` int(11) DEFAULT NULL,
  `score` int(11) DEFAULT NULL,
  `win` tinyint(1) DEFAULT NULL,
  `loss` tinyint(1) DEFAULT NULL,
  `createdAt` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_results_games` (`gameId`),
  KEY `fk_results_teams` (`teamId`),
  CONSTRAINT `fk_results_games` FOREIGN KEY (`gameId`) REFERENCES `games` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `fk_results_teams` FOREIGN KEY (`teamId`) REFERENCES `teams` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

CREATE TABLE IF NOT EXISTS `teams` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `gameId` int(11) DEFAULT NULL,
  `win` tinyint(1) DEFAULT NULL,
  `loss` tinyint(1) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_teams_games` (`gameId`),
  CONSTRAINT `fk_teams_games` FOREIGN KEY (`gameId`) REFERENCES `games` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

CREATE TABLE IF NOT EXISTS `teams_players` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `teamId` int(11) DEFAULT NULL,
  `playerId` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_teams_players_players` (`teamId`),
  KEY `fk_teams_players_teams` (`playerId`),
  CONSTRAINT `fk_teams_players_players` FOREIGN KEY (`playerId`) REFERENCES `players` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `fk_teams_players_teams` FOREIGN KEY (`teamId`) REFERENCES `teams` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
