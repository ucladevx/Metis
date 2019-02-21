const express = require('express');
const mongoose = require('mongoose');
var router = express.Router();

// functions called by API endpoints
const helpers = require('../helpers/functions');

require('../schemas/PreRequisites.js');
const PreRequisitesSchema = mongoose.model('PreRequisites');

router.post('/test/', (req,res)=> {
  res.send("Welcome, " + req.body.name);
});

router.post('/testjson', (req,res)=> {
  res.send(req.body.name + " " + req.body.age);
});

router.post('/post-prereq', function(req, res, next) {
  for (var i = 0; i < req.body.list.length; i++) {
    var obj = req.body.list[i];
    var p = new PreRequisitesSchema({
      class_name: obj.name,
      class_prerequisites: obj.prereqs,
      class_corequisites: obj.coreqs,
    })
    p.save();
  }
  res.send("Success");
});

module.exports = router;
