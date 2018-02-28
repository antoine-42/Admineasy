var Methode = {

    parcourirResultat: function(requete){
    
        console.log("parcourirResultat METHODE");
        if(requete.readyState==4 && requete.status==200){
			console.log("RESP: "+requete.responseText);
			var maReponse=requete.responseText;
			
			for (var i = 0 ; i < maReponse.length; i++){
				if(maReponse.charAt(i)=='<'){
					i++;
					if(maReponse.charAt(i)=='a'){
						i++;
						if(maReponse.charAt(i)==' '){
							console.log("AFFICHER IMAGE ");

							Methode.afficherMachine();
						}
					}
				}
			}
		}
	},

	afficherMachine: function(){
		var  elem=document.getElementById("texte");  // recupere la ou on va modif
		var machine=document.getElementById("machine");  
		var image= new Image();
		/*image.onload=function () {
				image.src="./img/computer.png";
		}
		image.src="./img/computer.png";  // charge notre image*/

		image.src=machine.class;

		image.style.color="red";
		var div = document.createElement("div");
		div.style.display= "block";
		div.appendChild(image);
		elem.appendChild(div);
		


	},

	searchListMachine: function(){
		console.log("searchListMachine METHODE");
		var requete= creerRequete();
		var url="http://nailyk.ddns.net:54823/listreseau" ;
		requete.open("POST", url, true);
		requete.onreadystatechange=function(){
			Methode.parcourirResultat(requete);
		}

		requete.send();
		},
	 
};

/*********************************************************************************/

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

};
