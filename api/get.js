const express = require('express');
var router = express.Router();

// functions called by API endpoints

router.get('/test/:name', (req,res)=> {
  res.send("Welcome, " + req.params.name);
});

module.exports = router;
