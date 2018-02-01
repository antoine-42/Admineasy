var Accueil = {
	nbAlertes: 7,

	setAlerte: function(){
		this.nbAlertes++;
	},

	afficherAlerte: function(){
		if(this.nbAlertes==0){
			document.getElementById("alerte").style.color="green";
			document.getElementById("texte").innerHTML += "<br><p>Il n'y a pas d'alerte</p>";
			
		}else if(this.nbAlertes==1){
			document.getElementById("alerte").style.color="orange";
			document.getElementById("texte").innerHTML += "<br><p>Il y a 1 alerte</p>";

		}else if(this.nbAlertes>1){
			document.getElementById("alerte").style.color="red";
			document.getElementById("texte").innerHTML += "<br><p>Il y a "+this.nbAlertes+" alertes</p>";
		}

	},

};
