<?php

<?php

	if(isset($_POST['modele'])){
		$element=$_POST['modele'];
	}else{
		$element="raté";
	}

try{
	$bdd = new PDO('mysql:host=localhost;dbname=dacostam;charset=utf8', 'root', '');
}catch (Exception $e){
        die('Erreur : ' . $e->getMessage());
}

	$retour = "";
	$reponse = $bdd->query("SELECT * from Machines where CPU='$element'");

	while ($donnees = $reponse->fetch()){
		$retour= "<b>Machines: </b> Donnée: ".$donnees['Donnee']." CPU: " .$donnees['CPU']." valeur: ".$donnees['valeur']."<br>";

}
	echo $retour;
	$reponse->closeCursor(); // Termine le traitement de la requête
	
?>
