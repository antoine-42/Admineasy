<?php

	$element=$_POST["modele"];
	echo "ici: ".$element;
try{
	$conn = new PDO('mysql:host=localhost;dbname=cinema;charset=utf8', 'root', '');
	
}
catch (Exception $e){
        die('Erreur : ' . $e->getMessage());

}
	

	$query="select * from Machines where CPU-Modele LIKE '$element'";
	$result=mysql_query($conn, $query);

	$retour = "";

	while($row= mysql_fetch_assoc($result)){
		# code...
	
		$retour= "<b>Machines: </b>".$key['modele']."<br>";
	}

	echo $retour;

	mysql_free_result($result);
	mysql_close($conn);
?>