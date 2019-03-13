const express = require('express');
const mongoose = require('mongoose');
var router = express.Router();

// functions called by API endpoints
const helpers = require('../helpers/functions');

require('../schemas/PreRequisites.js');
const PreRequisitesSchema = mongoose.model('PreRequisites');

require('../schemas/ClassList.js');
const ClassListSchema = mongoose.model('ClassList');

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

router.post('/post-classlist', function(req, res, next) {
  var obj = req.body.classes;
  var p = new ClassListSchema({
    classes: obj,
  })
  p.save();
  res.send("Success");
});

// router.post('/get-prereq', function(req, res, next) {
//   // req: 
//   // res: json containing prereqs of class
//   PreRequisitesSchema.find({class_name: req.class_name}, function(err, result){
//     var class_object = {};

//     result.forEach(function(obj) {
//       class_object[user._id] = obj;
//     });

//     res.send(class_object); 
//   });
// });

module.exports = router;
