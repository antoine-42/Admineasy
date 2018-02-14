<?php

	if(isset($_POST['modele'])){
		$element=$_POST['modele'];
	}else{
		$element="raté";
	}

/*try{
	$bdd = new PDO('mysql:host=localhost;dbname=dacostam;charset=utf8', 'dacostam', 'dacostam');
}catch (Exception $e){
        die('Erreur : ' . $e->getMessage());
}

	$retour = "";
	$reponse = $bdd->query("SELECT * from Machines where CPU-Model='$element'");

	while ($donnees = $reponse->fetch()){
		$retour= "<b>Machines: </b> Donnée: ".$donnees['Donnee']." CPU: " .$donnees['CPU']." valeur: ".$donnees['valeur']."<br>";

}
	echo $retour;
	$reponse->closeCursor(); // Termine le traitement de la requête
	
	*/

// influx


$client = new \crodas\InfluxPHP\Client(
   "10.8.0.1",  //host
   8086,   //port
   "admineasy-client",  //user
   "1337"   //password
);


//$db= $client->admineasy;
$db = $client->getDatabase("admineasy");

echo "PHP";

foreach ($db->query("SELECT * FROM ram") as $row) {

	var_dump($row, $row->time);
}

?>