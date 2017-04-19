use mapdb_db;

drop table if exists anecdotes;
drop table if exists wellesley_people;

create table wellesley_people(
	pid int auto_increment primary key, 
	-- ^ perhaps email alias/username, not auto_increment int
	nm varchar(30) not null,
	email varchar(22) not null, -- wwellesle@wellesley.edu
	username varchar(8) not null,
	password varchar(50) not null, -- encrypted eventually?
	yr int, -- graduation year! :D 
	num_anecdotes int default 0 -- starts as 0
	)
	-- table constraint
	ENGINE = InnoDB;

create table anecdotes(
	aid int auto_increment primary key,
	content varchar(300) not null, -- parse #tags and @usernames later
	lat float(9,6) not null,
	lng float(9,6) not null,
	pid int not null,
	INDEX (pid),
	foreign key (pid) references wellesley_people(pid) on delete cascade
	)
	-- table constraint
	ENGINE = InnoDB; 

# ANONYMOUS user
INSERT into wellesley_people values (1, 'Wendy Wellesley','wwellesl@wellesley.edu','wwellesl','wendy4prez',1993,0);