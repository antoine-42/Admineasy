var Methode = {
	 searchIP: function(){
		var requete= creerRequete();
		var arg=document.getElementById("ip").value;
		var url="http://nailyk.ddns.net:54823/machine?ip="+arg ;
		requete.open("POST", url, true);
		requete.onreadystatechange=function(){
			afficherResultat(requete);
		}

		requete.send();
		},

		search: function(){
		var requete= creerRequete();
		var url="http://nailyk.ddns.net:54823/listmachine" ;
		requete.open("POST", url, true);
		requete.onreadystatechange=function(){
			afficherResultat(requete);
		}

		requete.send();
		},


	  afficherResultat: function(requete){
	 		console.log("afficherResultat");
		if(requete.readyState==4 && requete.status==200){
			console.log("afficherIIIFFFF");
			elem=document.getElementById("texte");
			console.log("RESP: "+requete.responseText);
			elem.innerHTML=requete.responseText;
		}
	},
}