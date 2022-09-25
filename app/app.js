const express = require("express");
const { get } = require("request");
const request = require("request")

const app = express();
const PORT = 3000;

app.get("/", (_req, _res) => {
   _res.status(200).send("ping");
});

app.get("/sync", (_req, _res) => {
    request("http://bbox:9090", {json:true}, (err, response, body) => {
        if (err) {return console.log(err);}
        _res.status(200).send(`Sync: ${body}`);
    });
});

app.get("/async", (_req, _res) => {
    request("http://bbox:9091", {json:true}, (err, response, body) => {
        if (err) {return console.log(err);}
        _res.status(200).send(`Async: ${body}`);
    });
});

app.get('/heavy', (_req,_res) => {
    for (t = new Date(); new Date() - t < 100; );
    _res.status(200).send("heavy");
});

app.listen(PORT, () => {
    console.log("Escuchando en el puerto", PORT)
});