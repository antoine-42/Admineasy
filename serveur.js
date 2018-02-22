/**Variables**/
var PORT = 54823 ; //Port d'écoute

/*Modules*/
var http = require("http") ;								//Module pour communiquer en HTML
var url = require("url") ;									//Module pour gérer les URL
var querystring = require("querystring") ;					//Module pour analyser une requete
var pg = require("/home/invite/js_node/node_modules/pg") ;						//Module pour se connecter à Postgres
var ping = require("/home/invite/js_node/node_modules/ping") ;


/*****************************************************/
var ping_machine = function (ip, callback)
{
	ping.sys.probe(ip, function(isAlive)
						{
    						var retour = isAlive ? ip + ' connecté' : ip + ' deconnecté' ; //Structure de if simplifiée
    						callback(retour);
						}) ;
	
}

var machine_get = function(ip, callback)
	{
		console.log("ENTRER MACHINE GET");
		var conString = "postres://admineasy_client:1337@10.8.0.1:5432/admineasy" ;

		var client = new pg.Client(conString) ;
		client.connect(err =>
						{if(err)
							{
								console.log("Attente de connexion") ;
								throw err ;
							}
						});

	console.log("IP: "+ip);
		var query = "select * from machines where local_ip='"+ip+"'" ;
console.log("APRES QUERY");
		client.query(query).then(res =>
								{
									
									var rows = res.rows ;
									console.log("rows: "+rows);
									if(rows[0]==undefined) {
										console.log("IF: rows[0]=" +rows[0]);
										callback("IP inexistante "+ip);
									}else{

									rows.map(row =>
											{
												console.log("rows map");
												var retour = `${JSON.stringify(row)}` ;
												/*
													Formatez le retour en HTML comme vous le souhaitez.
													Pour le moment, je ne renvoie que la ligne suivante, mais ça vous permet de voir les champs pour composer le retour HTML.

													{"name":"antoine_main","os_complete":"Windows-10-10.0.16299-SP0","os_simple":"Windows","os_version":"10","user_name":"Antoin","connection_time":"2018-02-20T00:07:57.000Z","cpu_name":"Intel(R) Core(TM) i7-5820K CPU @ 3.30GHz","cpu_cores":6,"cpu_threads":12,"cpu_hyperthreading":true,"cpu_freqmin":0,"cpu_freqmax":3300,"ram_total":17070,"swap_total":22438,"local_ip":"192.168.1.42","net_ifaces":"EthernetEthernet 2Loopback Pseudo-Interface 1Local Area Connection* 10","disk_names":"C:\\D:\\"}

													Attention, cas non traité : si le retour est vide (adresse IP non connue)
														Dans ce cas, le serveur renvoit la ligne... donc rien
												*/
												console.log("RETOUR "+retour);

												callback(retour) ;

											}) ;
									}
								})
							.catch(err =>
								{
									console.log(err) ;
									callback("<b>Une erreur est survenue lors de la requete.")
								}) ;
							
							console.log("FIIIIIIINNNNNNNN");


	}

var ping_get = function(callback)
				{
					var conString = "postres://admineasy_client:1337@10.8.0.1:5432/admineasy" ;
					var client = new pg.Client(conString) ;
					client.connect(err =>
									{if(err)
										{
											console.log("Attente de connexion") ;
											throw err ;
										}
									});

					var query = "select * from connected" ;

					client.query(query).then(res =>
									{
										var rows = res.rows ;
										var retour = "<ul>" ;
										rows.map((row) =>
												{
													//console.log(`Lecture : ${JSON.stringify(row)}`) ;
													retour+='<li> date : '+row.date+' -- ip : '+row.ip+'</li>' ;
												});
										retour+='</ul>' ;
										//console.log("Row : "+retour) ;
										callback(retour)	;
									});
				}

/*Fonction d'affichage du code HTML
 *	@params html 			//Contient le code HTML à afficher
 */
var ecrire_HTML = function(html, res)
					{
							
							console.log("Retour fonction : "+html) ; //Log serveur
			
							/*Création de l'HTML*/
							res.writeHead(200, {"Content-Type": "text/html"}) ; 	//Code de retour indiquant que la page fonctionne (404 --> non trouvée...), type de retour(html, image...)
							res.write(html) ;
							res.end() ;

					}
/*********************************************************/

/*Réaction lors de l'appel de la page
 * @params req		//Informations au sujet de la page appelée, des paramètres, des champs de requete formulaire [...]
 * @params res		//Variable contenant le retour de la fonction (code HTML à afficher)
 */
var reaction = function(req, res)
				{
					res.setHeader('Access-Control-Allow-Origin', '*') ; //Autorise tout le monde à accèder au serveur
					var codeHtml ; //Chaine de caractères à écrire
					
					var page = url.parse(req.url).pathname ;	//Permet de savoir quelle page est demandée.

					if(page == '/ping')
					{
						var arguments = querystring.parse(url.parse(req.url).query) ;		//On récupère et on on segmente les arguments dans un tableau
						if('ip' in arguments)
						{
							console.log(arguments['ip']) ;
							var retour_ping = ping_machine(arguments['ip'], function(html)
																			{
																				ecrire_HTML(html, res) ;
																			}) ;
							
						}
						else
						{
							ping_get(function(html)
									{
										ecrire_HTML(html, res) ;
									}) ;
						}
					}
					else if(page == '/machine')
					{
						/**Traitement**/
						var arguments = querystring.parse(url.parse(req.url).query) ;		//On récupère et on on segmente les arguments dans un tableau
						if('ip' in arguments)
						{
							console.log(arguments['ip']) ;
							console.log("MACHINE IP");
							machine_get(arguments['ip'], function(html)
															{
																ecrire_HTML(html, res) ;
															}) ;
						}
						else
						{
							ecrire_HTML("<b>Erreur</b>", res) ;
						}
					}
					else if(page != '/favicon.ico')
						{
							console.log(page) ;
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
server.listen(PORT) ; //Le serveur écoute le port 8888
console.log("Serveur lancé (port : "+PORT+")") ;
