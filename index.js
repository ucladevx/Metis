const bodyParser = require('body-parser');
const express = require('express');
const mongoose = require('mongoose');
const cors = require('cors')

var app = express();
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: true })); // support encoded bodies
app.use(cors());

// api routes
app.use('/api', require('./api/get'));

// routes to post data
app.use('/post', require('./api/post'));

// routes to scrape and update db
app.use('/scrape', require('./api/scrape'));

app.get('/', (req,res) => {
  res.send("Welcome to BH Backend")
})

app.listen(process.env.PORT || 3000, () => {
	console.log("listening on port 3000");
});
