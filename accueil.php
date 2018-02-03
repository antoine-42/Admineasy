<?php

echo "AAAAAAAAAAAAAAAAAAAAAAAAA";
	if(isset($_POST['modele'])){
		echo "IFF";
		$element=$_POST['modele'];
	}else{
		$element="raté";
	}
	echo "ici: ".$element;



    $bdd = mysql_connect("localhost", "root", "");
    mysql_select_db("dacostam");

    $query="SELECT * from Machines where CPU='$element'";
    $result=mysql_query($query);

	/*$query2="UPDATE Machines set valeur =valeur+1 where CPUModele LIKE '$element'";
	
	$res=mysql_query($query2);
	*/


	$retour = "";

	while($row=mysql_fetch_assoc($result)){
	
		$retour= "<b>Machines: </b>".$row['Donnee'] .$row['CPU'].$row['valeur']."<br>";
	}

	echo $retour;

	mysql_free_result($result);
	mysql_close($bdd);

	

	
?>