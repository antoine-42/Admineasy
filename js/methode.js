var Methode = {

    parcourirResultat: function(requete){
    
        console.log("parcourirResultat METHODE");
        if(requete.readyState==4 && requete.status==200){
			console.log("RESP: "+requete.responseText);
			var maReponse=requete.responseText;
			
			for (var i = 0 ; i < maReponse.length; i++){
				if(maReponse.charAt(i)=='<'){
					if(maReponse.charAt(i+1)=='a'){
						if(maReponse.charAt(i+2)==' '){
							console.log("AFFICHER IMAGE ");

							Methode.afficherMachine();
						}
					}
				}
			}
		}
	},

	afficherMachine: function(){
	elem=document.getElementById("texte");
		var image= new Image();

		image.onload=function () {
			image.src="~/mack/admineasy/img/computer.png";
		}
		image.src="~/mack/admineasy/img/computer.png";

		elem.innerHTML=image;

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