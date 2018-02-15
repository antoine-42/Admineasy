var pg = require('/home/invite/js_node/node_modules/pg') ;
var conString = "postres://admineasy_client:1337@10.8.0.1:5432/admineasy" ;

var client = new pg.Client(conString) ;
client.connect() ;

var query = client.query("select * from machines") ;
console.log("ca marche") ;

query.on('row', function(row)
				{
					console.log(row) ;
				}) ;

query.on('end', function(end)
				{
					client.end() ;
				}) ;
