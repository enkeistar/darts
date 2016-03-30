# Darts

## Setup

## Config
Create a config file here: ```/darts/config_file.cfg``` and specify the following parameters:
```
DEBUG=True
PORT=5000
MYSQL_USERNAME=''
MYSQL_PASSWORD=''
MYSQL_HOST=''
MYSQL_DATABASE=''
```

## TODO

* Redo player selection for x01 game mode
* better way to delete players from manage players screen, only admins, only if no stats?
* more better stats
* single and 3-player options
* varying number of games: single game, best of 3, best of 5, etc
* undo after game complete, or confirm end of game before proceeding
* individual game stats on game complete screen
* varying mark style?  have a library of mark options that can be pulled from

* http://flask.pocoo.org/docs/0.10/deploying/wsgi-standalone/



[3/25/2016 4:10:26 PM] Brett Meyer: Initial game selection is


Options for Cricket
	Best of 1
	Best of 3
	Best of 5

End game is
Quit | Play Again | Best of 1 | Best of 3 | Best of 5
[3/25/2016 4:11:13 PM] Brett Meyer: End game options keep teams and order the same, which player should start? next in order or go back to first?