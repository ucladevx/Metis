const bodyParser = require('body-parser');
const express = require('express');
const mongoose = require('mongoose');
const cors = require('cors')
require('dotenv').config();

// Database init and access functions
const db = require('./helpers/db.js')
const temp = require('./helpers/initDB.js')

// Create express app
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
  res.send("Welcome to Metis, the BM Backend")
})

// Connect to database, on success start server
db.initDb(function(err){
  temp.populateCourses()
  app.listen(process.env.PORT || 3001, () => {
  	console.log("server listening");
  });
});
