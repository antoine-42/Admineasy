var Methode = {

    afficherResultat: function(requete){
        console.log("afficherResultat METHODE");
        if(requete.readyState==4 && requete.status==200){
			console.log("");
		}
	},

	searchListMachine: function(){
		console.log("searchListMachine METHODE");
		var requete= creerRequete();
		var url="http://nailyk.ddns.net:54823/listmachine" ;
		requete.open("POST", url, true);
		requete.onreadystatechange=function(){
			this.afficherResultat(requete);
		}

		requete.send();
		},
	 
};