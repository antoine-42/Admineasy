

var Accueil = {
	nbAlertes: 0,

	setAlerte: function(){
		this.nbAlertes++;
	},

	afficherAlerte: function(){
		alerte=document.getElementById("alerte");
		if(this.nbAlertes==0){
			alerte.style.color="green";
			alerte.innerHTML += "<br><p>Il n'y a pas d'alerte</p>";
			
		}else if(this.nbAlertes==1){
			alerte.style.color="orange";
			alerte.innerHTML += "<br><p>Il y a 1 alerte</p>";

		}else if(this.nbAlertes>1){
			alerte.style.color="red";
			alerte.innerHTML += "<br><p>Il y a "+this.nbAlertes+" alertes</p>";
		}

	},

	/* search: function(){
		element=document.getElementById("modele").value;
		var requete= creerRequete();
		var url="accueil.php";

		requete.open("POST", url, true);
		requete.onreadystatechange=function(){
			afficherResultat(requete);
		}

		requete.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");

		requete.send("CPU-Modele"+ escape(element));
	},

	 afficherResultat: function(requete){
		if(requete.readyState==4 && requete.status==200){
			elem=document.getElementById("test");
			elem.innerHTML=requete.responseText;
		}
	}*/

};
