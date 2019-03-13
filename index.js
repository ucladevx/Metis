const bodyParser = require('body-parser');
const express = require('express');
const mongoose = require('mongoose');
const cors = require('cors')

var app = express();
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: true })); // support encoded bodies
app.use(cors());

// connect to Mongo
mongoose.connect('mongodb+srv://testuser:testpass@cluster0-gwzee.mongodb.net/test?retryWrites=true')
//mongoose.connect('mongodb://testuser:testpass@cluster0-shard-00-00-gwzee.mongodb.net:27017,cluster0-shard-00-01-gwzee.mongodb.net:27017,cluster0-shard-00-02-gwzee.mongodb.net:27017/test?ssl=true&replicaSet=Cluster0-shard-0&authSource=admin&retryWrites=true');

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
