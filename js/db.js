/*var pg = require('/home/invite/js_node/node_modules/pg') ;
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

*/
var sys = require("sys"),
my_http = require("http");
my_http.createServer(function(request,response){
  sys.puts("I got kicked");
  response.writeHeader(200, {"Content-Type": "text/plain"});
  response.write("Hello World");
  response.end();
}).listen(8080);
sys.puts("Server Running on 8080"); 