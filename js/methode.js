var Methode = {

    parcourirResultat: function(requete){
        console.log("parcourirResultat METHODE");
        if(requete.readyState==4 && requete.status==200){
			console.log("RESP: "+requete.responseText);
			var maReponse=requete.responseText;
			}
			/*for (int i = 0 ; i < maChaine.length() ;i++)
    			System.out.println(maChaine.charAt(i));
		}*/
	},

	searchListMachine: function(){
		console.log("searchListMachine METHODE");
		var requete= creerRequete();
		var url="http://nailyk.ddns.net:54823/listmachine" ;
		requete.open("POST", url, true);
		requete.onreadystatechange=function(){
			Methode.parcourirResultat(requete);
		}

		requete.send();
		},
	 
};