require('./js/methode.js');

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

/******************************************************************************************/

var machine_list_get = function(callback)
				{
					console.log("ENTRER MACHINE LIST GET");
					var conString = "postres://admineasy_client:1337@10.8.0.1:54823/admineasy" ;
					var client = new pg.Client(conString) ;
					client.connect(err =>
									{if(err)
										{
											console.log("Attente de connexion") ;
											throw err ;
										}
									});

					var query = "select * from machines" ;

					client.query(query).then(res =>
									{
										var rows = res.rows ;
										var retour = '<table><thead><tr>'
										+'<th>Nom Machine</th>'
										+'<th>IP Machine</th>'
										+'<th>Nom Utilisateur</th>'
										+'</tr></thead><tbody>';
										rows.map((row) =>
												{

												/*var requete= creerRequete();
												var url="http://nailyk.ddns.net:54823/machine?ip="+ip ;*
												var code=
												'<tr>'
												//+'<td><a href="javascript:Methode.searchIP('+retour[1]+')">'+retour[0]+'</a></td>'
												+'<td><a href="http://nailyk.ddns.net:54823/machine?ip='+retour[1]+'">'+retour[0]+'</a></td>'
												+'<td>'+retour[1]+'</td>'
												+'<td>'+retour[2]+'</td>'
												+'</tr>';*/

													//console.log(`Lecture : ${JSON.stringify(row)}`) ;
													retour+='<tr><td><a href="http://nailyk.ddns.net:54823/machine?ip='+row.local_ip+'">'
													+row.name+'</a></td><td>'+row.local_ip+'</td><td>'+row.user_name+'</td></tr>' ;
												});
										retour+='</tbody></table>' ;
										//console.log("Row : "+retour) ;
										callback(retour)	;
									})
					.catch(err =>
								{
									console.log(err) ;
									callback("<b>Une erreur est survenue lors de la requete.")
								}) ;
					console.log("FIIIIIIINNNNNNNN");

				}

	/******************************************************************************************/

var machine_get = function(ip, callback)  // recupere les machines correspondant à l'ip fournie
	{
		console.log("ENTRER MACHINE GET");
		var conString = "postres://admineasy_client:1337@10.8.0.1:5432/admineasy" ;  // connection a la BD

		var client = new pg.Client(conString) ;
		client.connect(err =>
						{if(err)
							{
								console.log("Attente de connexion") ;
								throw err ;
							}
						});

	console.log("IP: "+ip);
		var query = "select * from machines where local_ip='"+ip+"'" ;   // recupere les machines qui ont l'ip demande
console.log("APRES QUERY");
		client.query(query).then(res =>
								{
									
									var rows = res.rows ;
									console.log("rows: "+rows);
									if(rows[0]==undefined) {  // si il n'ya pas de machines trouve
										console.log("IF: rows[0]=" +rows[0]);
										callback("IP inexistante "+ip);
									}else{
									rows.map(row =>
											{
												console.log("rows map");
												//var retour = `${JSON.stringify(row)}` ;
												
												/*
													Formatez le retour en HTML comme vous le souhaitez.
													Pour le moment, je ne renvoie que la ligne suivante, mais ça vous permet de voir les champs pour composer le retour HTML.

													{"name":"antoine_main","os_complete":"Windows-10-10.0.16299-SP0","os_simple":"Windows","os_version":"10","user_name":"Antoin",
													"connection_time":"2018-02-20T00:07:57.000Z","cpu_name":"Intel(R) Core(TM) i7-5820K CPU @ 3.30GHz","cpu_cores":6,"cpu_threads":12,
													"cpu_hyperthreading":true,"cpu_freqmin":0,"cpu_freqmax":3300,"ram_total":17070,"swap_total":22438,"local_ip":"192.168.1.42",
													"net_ifaces":"EthernetEthernet 2Loopback Pseudo-Interface 1Local Area Connection* 10","disk_names":"C:\\D:\\"}

														Dans ce cas, le serveur renvoit la ligne... donc rien
												*/
												

												var retour = [];
												// remplie un tableau avec les caracteristiques
												retour[0]=row.name;
												retour[1]=row.local_ip;
												retour[2]=row.user_name;
												retour[3]=row.os_complete;
												retour[4]=row.os_simple;
												retour[5]=row.os_version;
												retour[6]=row.connection_time;
												retour[7]=row.cpu_name;
												retour[8]=row.cpu_cores;
												retour[9]=row.cpu_threads;
												retour[10]=row.cpu_hyperthreading;
												retour[11]=row.cpu_freqmin;
												retour[12]=row.cpu_freqmax;
												retour[13]=row.ram_total;
												retour[14]=row.swap_total;
												retour[15]=row.net_ifaces;
												retour[16]=row.disk_names;

												console.log("RETOUR "+retour);

												var code=
												'<li>Nom Machine : '+retour[0]+'</li>'  // affichage des caracteristique en liste
												+'<li>IP Machine : '+retour[1]+'</li>'
												+'<li>Nom Utilisateur : '+retour[2]+'</li>'
												+'<li>OS Complet : '+retour[3]+'</li>'
												+'<li>OS Simple : '+retour[4]+'</li>'
												+'<li>OS Version : '+retour[5]+'</li>'
												+'<li>Connection Time : '+retour[6]+'</li>'
												+'<li>CPU Name : '+retour[7]+'</li>'
												+'<li>CPU Cores : '+retour[8]+'</li>'
												+'<li>CPU lireads : '+retour[9]+'</li>'
												+'<li>CPU Hyperlireading : '+retour[10]+'</li>'
												+'<li>CPU Freqmin : '+retour[11]+'</li>'
												+'<li>CPU Freqmax : '+retour[12]+'</li>'
												+'<li>RAM Total : '+retour[13]+'</li>'
												+'<li>Swap Total : '+retour[14]+'</li>'
												+'<li>Net Ifaces : '+retour[15]+'</li>'
												+'<li>Disk Names : '+retour[16]+'</li>';

												callback('<ul>'+code+'</ul>') ;

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
	/******************************************************************************************/

var ping_get = function(callback)  // recupere les machines connecte
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

					var query = "select * from connected" ;  // toutes les machines qui sont dans l'état "connecte" dans la bd

					client.query(query).then(res =>
									{
										var rows = res.rows ;
										var retour = "<ul>" ;
										rows.map((row) =>
												{
													//console.log(`Lecture : ${JSON.stringify(row)}`) ;
													// affichage
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
							console.log("header");
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
					else if(page == '/listmachine')
						{
							console.log("PAGE LIST MACHINE");
							machine_list_get(function(html)
									{
										ecrire_HTML(html, res) ;
									}) ;

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
