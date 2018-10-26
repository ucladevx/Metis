const bodyParser = require('body-parser');
const express = require('express');
const mongoose = require('mongoose');
const cors = require('cors')

var app = express();
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: true })); // support encoded bodies
app.use(cors());

app.get('/', (req,res) => {
  res.send("Welcome to BH Backend")
})

app.listen(process.env.PORT || 3000, () => {
	console.log("listening on port 3000");
});
