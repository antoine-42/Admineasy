var Methode = {

    parcourirResultat: function(requete){
        console.log("parcourirResultat METHODE");
        if(requete.readyState==4 && requete.status==200){
			console.log("RESP: "+requete.responseText);
			var maReponse=requete.responseText;
			
			for (var i = 0 ; i < maReponse.length; i++){
    			console.log(maReponse.charAt(i));
			
			}
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