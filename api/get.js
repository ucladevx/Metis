const express = require('express');
const mongoose = require('mongoose');
var router = express.Router();

// functions called by API endpoints
const helpers = require('../helpers/functions');

router.get('/test/:name', (req,res  )=> {
  res.send("Welcome, " + req.params.name);
});

module.exports = router;
