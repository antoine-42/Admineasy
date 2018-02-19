
/**Variables**/
var PORT = 8888 ; //Port d'écoute

/*Modules*/
var http = require("http") ;								//Module pour communiquer en HTML
var url = require("url") ;									//Module pour gérer les URL
var querystring = require("querystring") ;					//Module pour analyser une requete
var pg = require("/home/invite/js_node/node_modules/pg") ;			//Module pour se connecter à Postgres

var mimeTypes = {
'.js': 'text/javascript',
'.html': 'text/html',
'.css': 'text/css'
};

var path = require('path');

var headers = {
                'Content-type': mimeTypes
            };
/*****************************************************/

var conString = "postres://admineasy_client:1337@10.8.0.1:5432/admineasy" ;

var client = new pg.Client(conString) ;
client.connect() ;

var query = client.query("select * from machines") ;

var list;

query.on('row', function(row)  // 
	{
		list = row ;  // on recupere ligne dans list
	}) ;
query.on('end', function(end)  // requette fini
	{
		client.end() ;  // on arrete le client
	}) ;

/*********************************************************/

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
						
						
        res.writeHead(200, headers);	//Code de retour indiquant que la page fonctionne (404 --> non trouvée...), type de retour(html, image...)
						//Prépare le code HTML
						codeHtml = '<!DOCTYPE html>'+
						'<html>'+
							'<head>'+
								'<meta charset="utf-8"/>'+
								'<link rel="stylesheet" href="https://fonts.googleapis.com/icon?family=Material+Icons">'+
								'<link rel="stylesheet" href="./css/style.css">'+
								'<script src="./js/accueil.js"></script>'+
								'<title>admineasy</title>'+
							'</head>'+
							'<body>'+
							'<header id="titre_principal">'+

								'<h1>AdminEasy</h1>'+
								'</header>'+
								'<nav>'+
								'<ul>'+
				'<li class="menuaccueil"><a href="index.html">Accueil</a></li>'+	
				'<li class="menureseau"><a href="reseau_vue.html">Réseau</a>'+			
				'</li>	'+
				'<li class="menumachines"><a href="machines_vue.html">Machines</a>'+
				'</li>'+
				'<li class="contact"><a href="contact_vue.html">Contact</a></li>'+	
			'</ul>'+
		'</nav>'+
		'<div id="accueil">'+
			'<i id="alerte" class="material-icons" style="font-size:48px;color:red">warning</i>'+
				
		'</div>'+

		'<div id="test">'+
		'<form id="monform">'+
				'CPU_Modele'+
				'<input id="modele" type="text"/>'+
				'<button>'+
				'Envoyer'+
				'</button>'+
			'</form>'+
		'</div>'+
		'<div id="texte"></div>'+
		'		<footer>  '+
			'<p class="gauchepdp">'+
				'MACK - Da Costa, Dujardin, Trugeon, Bohl'+
			'</p>'+
			'<p class="droitepdp">'+
				'<a href="contact_vue.html">Contact</a>'+
			'</p>'+
			
			'<p>'+
				'Projet dans le cadre du DUT informatique - IUT Fontainebleau - 2017/2018'+
			'</p>'+
			'<div style="clear : both"></div>'+
		'</footer>'+
							'</body>'+
						'</html>' ;

						res.write(codeHtml) ;

/***************************************************************************************/
						res.write("name : "+list.name+" os-simple : "+list.os_simple+" cpu-name : "+list.cpu_name);
/****************************************************************************************/
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