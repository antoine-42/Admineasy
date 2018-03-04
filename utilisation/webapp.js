"use strict";

//const path = require('path')
const express = require('express')
var bodyParser = require('body-parser');
var multer = require('multer'); // v1.0.5
var upload = multer(); // for parsing multipart/form-data

const Influx = require('influx')
const influx = new Influx.InfluxDB('http://10.8.0.1:8086/admineasy')

const app = express()

app.use(express.static('public'));
app.use(express.static('js'));
// https://codeforgeek.com/2014/09/handle-get-post-request-express-4/

app.use(bodyParser.urlencoded({ extended: true })); // for parsing application/x-www-form-urlencoded
app.use(bodyParser.json()); // for parsing application/json

app.get('/', function (req, res) {
  res.redirect('/index.html')
})

app.post('/time_cpu', upload.array(), function(req, res, next) {
    // period is expressed in seconds to ease updates
    var limit=(Date.now()-req.body.cpu_period*1000)*1e6;
    var db_rq = "select time,used from cpu where machine='"+req.body.cpu_machine+"' and time>"+limit+" order by time";

    influx.query(db_rq)
        .then(results => { 
                 res.json(results);
              }
             )
});
// app.post('/time_cpu', upload.array(), function(req, res, next) {
/*
app.get('/time_cpu', bodyParser.json(deflate=true, type='* / *'), function(req, res, next) {
    console.log('received '+req.body.cpu_machine);
    limit=Date.now()-req.body.cpu_period*3600000;
    influx.query("select time,used from cpu where machine='"+req.body.cpu_machine+"' and time>'+limit+' order by time")
        .then(results => { 
                 res.json(results);
              }
             )


//    res.send('Hello '+req.body.name+' from '+req.body.city);
})
*/

const parser=express.json()

app.get('/time_cpu', function(req, res) {
    console.log(req.cpu_period);
    var myjs=parser(req.body);
    console.log(myjs);
    res.json({rep:'hello'});
})

app.listen(3000, function () {
  console.log('Example app listening on port 3000!')
})

