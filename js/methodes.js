var Methode = {

    parcourirResultat: function(requete){
   
        console.log("parcourirResultat METHODE");
        if(requete.readyState==4 && requete.status==200){
			console.log("RESP: "+requete.responseText);
			var maReponse=requete.responseText;
			 elem=document.getElementById("texte");
			var j=0;
			for (var i = 0 ; i < maReponse.length; i++){  
			// parcours la reponse evoyé par le serveur
			// qui ressemble à plusieurs lien comme ça:
		// <a href="http://nailyk.ddns.net:54823/machine?ip=127.0.1.1">127.0.1.1</a>

				if(maReponse.charAt(i)=='<'){
					i++;
					if(maReponse.charAt(i)=='/'){
						i++;
						if(maReponse.charAt(i)=='a'){
							i++;
							if(maReponse.charAt(i)=='>'){ // des quel detecte la fin d'une balise a
								console.log("AFFICHER IMAGE ");
								elem.innerHTML+=maReponse.substring(j, i);  
								// affiche la partie de la reponse du serveur
								// qui correspond à un lien 
								j=i+1;  // pour decaler la partie que l'on va afficher
								Methode.afficherMachine();  
								// affiche l'image du computer
								// sous le lien correspondant
							}
						}
					}
				}
			}
		}
	},

	afficherMachine: function(){
		var  elem=document.getElementById("texte");  // recupere la ou on va modif
		var image= new Image();  // creer object image
		/*image.onload=function () {
				image.src="./img/computer.png";
		}*/

		if(Machine.etat=="connected"){  // verifie l'etat de la machine
			image.src="./img/computergreen.png";  // donne le lien de l'image correspondant a letat de la machine
		}else if(Machine.etat=="problem"){
			image.src="./img/computerred.png"; 
		}else{
			image.src="./img/computer.png";
		}
	
		var div = document.createElement("div");  // creer une div
		div.style.display= "block";  // la met en block pour que chaque image soit en dessous
		div.appendChild(image);  // donne a la div l'image
		elem.appendChild(div);  // met la nouvelle div la ou on veut dans notre html


	},

	searchListReseau: function(){
		console.log("searchListMachine METHODE");
		var requete= creerRequete();
		var url="http://nailyk.ddns.net:54823/listreseau" ;
		requete.open("POST", url, true);
		requete.onreadystatechange=function(){
			Methode.parcourirResultat(requete);
		}

		requete.send();
		},


	searchIP: function(){
		console.log("searchIP");
		var requete= creerRequete();
		var arg=document.getElementById("ip").value;
		var url="http://nailyk.ddns.net:54823/machine?ip="+arg ;
		requete.open("POST", url, true);
		requete.onreadystatechange=function(){
			afficherResultat(requete, arg, "IP");
		}

		requete.send();
		},

	searchListMachine : function(){
		Machine.effacerMachine(); // n'affiche plus l'icone machine quand on affiche la liste
		console.log("searchListMachine");
		var requete= creerRequete();
		var url="http://nailyk.ddns.net:54823/listmachine" ;
		requete.open("POST", url, true);
		requete.onreadystatechange=function(){
			afficherResultat(requete, null, "List");
		}

		requete.send();
		},


		afficherResultat : function(requete, ip, provenance){
	 	console.log("afficherResultat");
		if(requete.readyState==4 && requete.status==200){
			console.log("RESP: "+requete.responseText);
			elem=document.getElementById("texte");
			if(requete.responseText=="null"){// si pas trouve d'IP
				elem.innerHTML="IP:  "+ip+" est inexistante";
				Machine.effacerMachine();

			}else if(provenance=="List"){  // si est appelé par searchListMachine
				elem.innerHTML=requete.responseText;

			}else{  // si est appelé par searchIP
				elem.innerHTML=requete.responseText;
				Machine.afficherMachine();
			}	
		}
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

/***************************************************************************************/

var Machine = {
	 etat: "connected",

	setEtat: function(et){
		this.etat=et;
	},

	afficherMachine: function(){
		console.log("AFFICHER MACHINE");
		machine=document.getElementById("machine");
		machine.style.display="inline";
		if(this.etat=="connected"){
			machine.style.color="green";
			
		}else if(this.etat=="problem"){
			machine.style.color="orange";
		}else{
			machine.style.color="grey";
		}

	},

	effacerMachine: function () {
		machine=document.getElementById("machine");
		machine.style.display="none";
	},

};