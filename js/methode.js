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
	machine=document.getElementById("machine");
		var image= new Image();

		/*image.onload=function () {
			image.src="./img/computer.png";
		}
		image.src="./img/computer.png";*/

		image.onload=function () {
			image.src="./img/computer.png";
		}
		image.src="./img/computer.png";

		/*image.onload=function () {
			image.src=machine;
		}
		image.src=machine;*/

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