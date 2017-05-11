<!DOCTYPE html>
<html>
	<head></head>
	<body>

		<?php 
			require_once("/home/cs304/public_html/php/DB-functions.php");
			print "EHLLOOO are you theeerrree";

			$aid = intval($_REQUEST['aid']);
			print $aid;
			$mngo_nday_dsn = array ('hostspec' => 'localhost',
							'username' => 'mapdb',
							'password' => 'nnmhNR33ETKuQAy',
							'database' => 'mapdb_db',
							'phptype' => 'mysql');
			// global variables
			$dbh = db_connect($mngo_nday_dsn);
			$self = $_SERVER['PHP_SELF'];

			// queries to add 1 to the likes column of particular anecdote
			$addlike_query = "UPDATE anecdotes set likes=likes+1 where aid=?";
			$addlike_resultset = prepared_query($dbh, $addlike_query, array($aid));

			header('Access-Control-Allow-Origin: *');
		?>
	</body>
</html>