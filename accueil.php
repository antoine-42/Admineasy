<?php

	/*if(isset($_POST['modele'])){
		$element=$_POST['modele'];
	}else{
		$element="raté";
	}*/

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

/*
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
*/

// postgre
///psql -d admineasy -U admineasy_client -h 10.8.0.1

echo "ici";
// Connexion, sélection de la base de données
$dbconn = pg_connect("host=10.8.0.1 dbname=admineasy user=admineasy-client password=1337")
    or die('Connexion impossible : ' . pg_last_error());

// Exécution de la requête SQL
$query = "SELECT * FROM Machines";
$result = pg_query($query) or die('Échec de la requête : ' . pg_last_error());

// Affichage des résultats en HTML
echo "<table>\n";
while ($line = pg_fetch_array($result, null, PGSQL_ASSOC)) {
    echo "\t<tr>\n";
    foreach ($line as $col_value) {
        echo "\t\t<td>$col_value</td>\n";
    }
    echo "\t</tr>\n";
}
echo "</table>\n";

// Libère le résultat
pg_free_result($result);

// Ferme la connexion
pg_close($dbconn);




?>