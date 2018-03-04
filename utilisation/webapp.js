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
  res.redirect('/index.html');
})

var types = {
    "cpu": {"usage": {"influx": "used"}, "freq": {"influx": "freq"}},
    "ram": {"usage": {"influx": "used_percent"}},
    "swap": {"usage": {"influx": "used_percent"}},
    "partition": {"usage-full": {"influx": "partition,total,used_percent"}}
};

for(var type in types){
    for(var mesure in types[type]){
        var id = type + "_" + mesure;

        app.post('/' + id, upload.array(), function(req, res, next) {
            // period is expressed in seconds to ease updates
            var param = req.url.substr(1).split("_");
            var limit=(Date.now()-req.body.cpu_period*1000)*1e6;
            var db_rq = "select time," + types[param[0]][param[1]]["influx"] + " from " + param[0] + " where machine='"+req.body.cpu_machine+"' and time>"+limit+" order by time";
            influx.query(db_rq)
                .then(results => {
                    res.json(results);
                }
            )
        });
    }
}

app.listen(3000, function () {
  console.log('app listening on port 3000!');
})

