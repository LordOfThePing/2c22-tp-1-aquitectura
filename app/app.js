const express = require("express");

const app = express();
const PORT = 3000;

app.get("/", (_req, _res) => {
   _res.status(200).send("ping prueba");
});

app.listen(PORT, () => {
    console.log("Escuchando en el puerto", PORT)
});