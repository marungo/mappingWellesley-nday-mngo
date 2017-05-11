<!DOCTYPE html>
<html>
	<head></head>
	<body>

		<?php 
			require_once("/home/cs304/public_html/php/DB-functions.php");

			$aid = intval($_GET['q']);
			$mngo_nday_dsn = array ('hostspec' => 'localhost',
							'username' => 'mapdb',
							'password' => 'nnmhNR33ETKuQAy',
							'database' => 'mapdb_db',
							'phptype' => 'mysql');
			// global variables
			$dbh = db_connect($mngo_nday_dsn);
			$self = $_SERVER['PHP_SELF'];

			// queries to add 1 to the likes column of particular anecdote
			$getlikes_query = "SELECT likes from anecdotes where aid=?";
			$addlike_query = "UPDATE anecdotes set likes=? where aid=?"; 

			$likes_resultset = prepared_query($dbh, $getlikes_query, [$aid]);
			$incrementedlikes = $likes_resultset->fetchOne()['likes'] + 1;

			$addlike_resultset = prepared_query($dbh, $addlike_query, [$incrementedlikes]);

		?>
	</body>
</html>