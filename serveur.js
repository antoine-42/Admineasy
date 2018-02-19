/**Variables**/
var PORT = 8888 ; //Port d'écoute

/*Modules*/
var http = require("http") ;								//Module pour communiquer en HTML
var url = require("url") ;									//Module pour gérer les URL
var querystring = require("querystring") ;					//Module pour analyser une requete
//var pg = require("pg") ;									//Module pour se connecter à Postgres


/*Réaction lors de l'appel de la page
 * @params req		//Informations au sujet de la page appelée, des paramètres, des champs de requete formulaire [...]
 * @params res		//Variable contenant le retour de la fonction (code HTML à afficher)
 */
var reaction = function(req, res)
				{
					var codeHtml ; //Chaine de caractères à écrire
					
					var page = url.parse(req.url).pathname ;	//Permet de savoir quelle page est demandée.

					if(page == '/')
					{
						/**Traitement**/
						var arguments = querystring.parse(url.parse(req.url).query) ;		//On récupère et on on segmente les arguments dans un tableau
						if('ip' in arguments)
							console.log(arguments['ip']) ;
						else
							console.log("Aucun argument") ;
							
							
						/**Affichage**/
						
						res.writeHead(200, {"Content-Type": "text/html"}) ; 	//Code de retour indiquant que la page fonctionne (404 --> non trouvée...), type de retour(html, image...)
						//Prépare le code HTML
						codeHtml = '<!DOCTYPE html>'+
						'<html>'+
							'<head>'+
								'<meta charset="utf-8"/>'+
								'<title>Caractéristiques</title>'+
							'</head>'+
							'<body>'+
								'<h1>Bonjour</h1>'+
									'<p>Ceci est un test</p>'+
							'</body>'+
						'</html>' ;
						
						res.write(codeHtml) ;
					}
					else if(page != '/favicon.ico')
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
					res.end() ;
				}

/*Le serveur est créé et on affiche le contenu souhaité*/
var server = http.createServer(reaction) ;
server.listen(PORT) ; //Le serveur écoute le port 8888
console.log("Serveur lancé (port : "+PORT+")") ;