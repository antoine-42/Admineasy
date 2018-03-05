/**Variables**/
var PORT = 54824 ; //Port d'écoute

/**Modules**/
var http = require("http") ;								//Module pour communiquer en HTML
var url = require("url") ;									//Module pour gérer les URL
var querystring = require("querystring") ;					//Module pour analyser une requete
var ping = require("./n/node_modules/ping") ;				//Module pour effectuer les pings

/*Exécute le ping d'une plage d'adresses IP
 *	@params byte1 et byte2				//Octects fixes dans les réseau privés (172.16.x.x ou 192.168.x.x)
 *	@params byte3 et byte4 min/max		//Octets mobiles. Ils permettent de déterminer les adresses ip qui seront scannées
 *	@params callback					//Fonction permettant de retourner le résultat après exécution
 */
var ping_plage = function (byte1, byte2, byte3_min, byte3_max, byte4_min, byte4_max, callback)
				{
					//Préparations
					var liste = "" ;
					var preparation1, preparation2, preparation3 ;
					preparation1 = byte1+"."+byte2+"." ;

					//Les compteurs
					var i, j ;
					var compteur = 0 ;

					//Calcul le nombre d'opérations à effectuer
					var nbr_exec4 = (byte4_max-byte4_min)!=0 ? (byte4_max-byte4_min)+1 : 1 ;
					var nbr_exec3 = (byte3_max-byte3_min)!=0 ? (byte3_max-byte3_min)+1 : 1 ;
					var nbr_exec = nbr_exec3 * nbr_exec4 ;

					//Lancement des pings
					for(i=byte3_min ; i<=byte3_max ; i++)
					{
						preparation2 = preparation1+i+"." ;
						for(j=byte4_min ; j<=byte4_max ; j++)
						{
							preparation3 = preparation2+j ;
							ping_machine(preparation3, (retour)=>
																{
																	//Si l'appareil n'est pas déconnecté, on ajoute le retour
																	if(!(/deconnecté/.test(retour)))		//Expression regex <=> expression régulière. Entre / la chaine à cherche, puis test de la chaine dans laquelle chercher
																	{
																		liste+="<li>"+retour+"</li>" ;
																	}
																	compteur++ ;

																	//Lorsque toutes les exécutions sont effectuées, on appelle le callback
																	if(compteur == nbr_exec)
																		{
																			liste = "<ul>"+liste+"</ul>" ;
																			console.log("Machines testées : "+ nbr_exec) ;
																			callback(liste) ;
																		}
																}) ;
						}
					}
				}

/*Indique si la machine indiquée est connectée ou non au réseau
 *	@params ip 			//Ip de la machine à récupérer
 *	@params callback	//Fonction callback
 */
var ping_machine = function (ip, callback)
{
	ping.sys.probe(ip, function(isAlive)
						{
    						var retour = isAlive ? ip + ' connecté' : ip + ' deconnecté' ; //Structure de if simplifiée
    						callback(retour);
						}) ;	
}

/*Renvoie le résultat final de l'appel du serveur sous forme d'HTML
 *	@params html		//Chaine de caractères représentant le code HTML à retourner
 * 	@params res			//Objet de retour
 */
var ecrire_HTML = function(html, res)
					{		
							console.log("Retour fonction : "+html) ; //Log serveur
			
							/*Création de l'HTML*/
							res.writeHead(200, {"Content-Type": "text/html"}) ; 	//Code de retour indiquant que la page fonctionne (404 --> non trouvée...), type de retour(html, image...)
							res.write(html) ;
							res.end() ;
					}

var reaction = function(req, res)
				{
					res.setHeader('Access-Control-Allow-Origin', '*') ; //Autorise tout le monde à accèder au serveur
					var codeHtml ; //Chaine de caractères à écrire
					
					var page = url.parse(req.url).pathname ;	//Permet de savoir quelle page est demandée.

					if(page == '/ping')
					{
						var arguments = querystring.parse(url.parse(req.url).query) ;		//On récupère et on segmente les arguments dans un tableau
						if('ip' in arguments)
						{
							ping_machine(arguments['ip'], function(html)
																			{
																				ecrire_HTML(html, res) ;
																			}) ;
						}
						else
						{
							ping_plage(192, 168, 1, 2, 1, 255, function(html)
																{
																	ecrire_HTML(html, res) ;
																});
						}
					}
					else
					{
						res.writeHead(404, {"Content-Type": "text/html"}) ;
							//Prépare le code HTML
							codeHtml = '<!DOCTYPE html>'+
							'<html>'+
								'<head>'+
									'<meta charset="utf-8"/>'+
									'<title>404 Not Found</title>'+
								'</head>'+
								'<body>'+
									'<h1>404 Not Found</h1>'+
										'<p>Impossible de trouver la page</p>'+
								'</body>'+
							'</html>' ;
						
							res.write(codeHtml) ;
					}
				}

/*Le serveur est créé et on affiche le contenu souhaité*/
var server = http.createServer(reaction) ;
server.listen(PORT) ; //Le serveur écoute le port souhaité au début du code
console.log("Serveur lancé (port : "+PORT+")") ;

