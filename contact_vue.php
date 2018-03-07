<!DOCTYPE html>
<html lang="fr">
	<head>
		<meta charset="UTF-8" />
		<title>AdminEasy</title>
		<link rel='stylesheet' type='text/css' href='./css/style.css'>
	</head>
	<body>
		<header id="titre_principal">	
		<h1>AdminEasy</h1>	
		</header>


<?php

$nom = $_POST['nom'];
$prenom = $_POST['prenom'];
$email=$_POST['mail']
$objet=$_POST['objet'];
$message = $_POST['message'];





 
$to = 'mel-dacosta@hotmail.fr';
 
/* En-têtes de l'e-mail */
$headers = "From: $nom \r\n\r\n";
  
/* Envoi de l'e-mail */
mail($to, $objet, $message, $headers)
 
?>

		<!-- .....................................MENU........................................... -->
		<nav>  <!-- lien de navigation -->
			<ul>    <!-- accueil -->
				<li><a href="index.html">Accueil</a></li>	
				<li><a href="reseau_vue.html">Réseau</a></li>	
				<li><a href="machines_vue.html">Machines</a></li>
				<li><a href="utilisation_vue.html">Utilisation</a></li>
				<li class="selected"><a href="contact_vue.html">Contact</a></li>	
			</ul>
		</nav>
		
<!-- ......................................... CONTACT ............................................ -->
			<div class="contact">
				<br/>
				<h2>Envoyer un message</h2>
				<br/>
				<h4>Pour toute demande, question ou information, n'hésitez pas à utiliser le formulaire de contact ci-dessous.</h4>
				<br/>
				<div class="contact_form">
				<form method="post">
					<fieldset>
						<legend>Formulaire de contact</legend>
						<p>
							<label for="prenom">Prénom :</label>
							<input type="text" name="prenom" id="prenom" placeholder="Ex : Jane" required>
						</p>
						<br/>
						<p>
							<label for="nom">Nom :</label>
							<input type="text" name="nom" id="nom" placeholder="Ex : Doe" required>
						</p>
						<br/>
						<p>
							<label for="nom">Adresse email :</label>
							<input type="email" name="mail" id="mail" placeholder="Ex : janedoe@email.fr" required>
						</p>
						<br/>
						<p>
							<label for="nom">Objet :</label>
							<input type="text" name="objet" id="objet">
						</p>
						<br/>
						<p>
							<label for="message">Message :</label>
							<textarea name="message" id="message" rows="10" cols="50"></textarea>
						</p>
						<br/><br/>
						<div id="contact_button">
							<input type="submit" value="Envoyer"/>
							<input type="reset" value="Effacer"/>
						</div>
					</fieldset>
				</form>
				</div>
			</div>
		

<!-- ........................................... PIED DE PAGE ..................................... -->
		<footer>  
			<p class="gauchepdp">
				MACK - Da Costa, Dujardin, Trugeon, Bohl
			</p>
			<p class="droitepdp">
				<a href="contact_vue.html">Contact</a>
			</p>
			
			<p>
				Projet dans le cadre du DUT informatique - IUT Fontainebleau - 2017/2018
			</p>
			<div style="clear : both"></div>
		</footer>
	</body>
</html>