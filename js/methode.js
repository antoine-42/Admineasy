var Methode = {

    parcourirResultat: function(requete){
    	machine=document.getElementById("machine");
        console.log("parcourirResultat METHODE");
        if(requete.readyState==4 && requete.status==200){
			console.log("RESP: "+requete.responseText);
			var maReponse=requete.responseText;
			
			for (var i = 0 ; i < maReponse.length; i++){
				if(maReponse.charAt(i)=='<'){
					console.log("IMAGE "+maReponse.charAt(i));
					if(maReponse.charAt(i+1)=='a'){
						console.log("AAAAAAAAA  i= "+i+"   "+maReponse.charAt(i+1));
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

		var image= new Image();

		image.onload=function () {
			image.src="./img/computer.png";
		}


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