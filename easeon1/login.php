<!DOCTYPE html>
<head>
</head>
<body>
<?php
error_reporting(0);
session_start();
$conn = @mysql_connect("localhost","giri","1234");
  if(!$conn)
  {
     die("cannot connect:" . mysql_error());	
  }
	mysql_select_db("easeon",$conn);

$id = $_POST["email"];
$pwd = $_POST["pin"];
$select = mysql_query("select * from login where email = '$id' and pin = '$pwd'");
$select1 = mysql_fetch_array($select);
$rows = mysql_num_rows($select);
if($rows != 1)
{
echo "invalid username and password";
}
else
{
$_SESSION["username"] = $id;
$_SESSION["pwd"] = $pwd;
header("location:index.php");
}

?>
</body>
</html>
