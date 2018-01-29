var Accueil = {
	nbAlertes: 2,

	setAlerte: function(){
		this.nbAlertes++;
	},

	afficherAlerte: function(){
		if(this.nbAlertes==0){
			document.getElementById("alerte").src="./img/ok.png";
			document.getElementById("texte").innerHTML += "<br><p>Il n'y a pas d'alerte</p>";
			
		}else if(this.nbAlertes==1){
			document.getElementById("alerte").src="./img/moy.jpg";
			document.getElementById("texte").innerHTML += "<br><p>Il y a 1 alerte</p>";

		}else if(this.nbAlertes>1){
			document.getElementById("alerte").src="./img/bad.png";
			document.getElementById("texte").innerHTML += "<br><p>Il y a "+this.nbAlertes+" alertes</p>";
		}

	},

};
