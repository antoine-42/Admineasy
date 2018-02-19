var pg = require('/home/invite/js_node/node_modules/pg') ;
var conString = "postres://admineasy_client:1337@10.8.0.1:5432/admineasy" ;

var client = new pg.Client(conString) ;
client.connect() ;

var query = client.query("select * from machines") ;

var list;

query.on('row', function(row)
	{
		list = row ;
	}) ;
query.on('end', function(end)
	{
		client.end() ;
	}) ;




var http = require("http");
http.createServer(function(request,response)
{
  response.writeHead(200, {"Content-Type": "text/plain"});

  console.log(list);

  response.end("name : "+list.name+" os-simple : "+list.os_simple+" cpu-name : "+list.cpu_name);
  console.log(list.name);
  console.log(list.os_simple);
  console.log(list.cpu_name);
}).listen(8080,'192.168.1.21');
console.log("Server Running at http://192.168.1.21:8080/"); 
