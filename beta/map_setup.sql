use mapdb_db;

drop table if exists anecdotes;
drop table if exists wellesley_people;

create table wellesley_people(
	username varchar(8) primary key,
	email varchar(22) not null, -- wwellesle@wellesley.edu
	nm varchar(30) not null,
	password varchar(100) not null, -- encrypted eventually?
	yr varchar(4) -- graduation year! :D 
	)
	-- table constraint
	ENGINE = InnoDB;

create table anecdotes(
	aid int auto_increment primary key,
	title varchar(100) not null,
	content varchar(300) not null, -- parse #tags and @usernames later
	likes int default 0 not null,
	lat float(9,6) not null,
	lng float(9,6) not null,
	username varchar(8) not null,
	anonymous tinyint(1) default 0 not null, -- 0: anecdote not anon; 1: anecdote is anon
	INDEX (username),
	foreign key (username) references wellesley_people(username) on delete cascade
	)
	-- table constraint
	ENGINE = InnoDB; 

# ANONYMOUS user
INSERT into wellesley_people values ('wwellesl','wwellesl@wellesley.edu','Wendy Wellesley','wendy4prez',1993);
INSERT into anecdotes values (1, "my title", "anecdote content",42.0,-71.3,"wwellesl", 0);
