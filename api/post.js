const express = require('express');
var router = express.Router();

// functions called by API endpoints
const helpers = require('../helpers/functions');

router.post('/test/', (req,res)=> {
  res.send("Welcome, " + req.body.name);
});

module.exports = router;
