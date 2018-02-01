

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
