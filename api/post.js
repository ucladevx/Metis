const express = require('express');
const mongoose = require('mongoose');
var router = express.Router();

// functions called by API endpoints
const helpers = require('../helpers/functions');

// acronym mapping
const mapping = require('../utils/acronym_mapping.json')

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

// router.post('/convertnames', function(req, res, next) {
//   var obj = req.body.classes;
//   var classes = []
//   for (let cls in obj) {
//     cls = obj[cls];
//     let department = mapping[cls.dept];
//     if (!department) {
//       console.log("ERROR: " + cls.dept + " is not a valid department name.");
//     }
//     let fullName = department + " " + cls.name;
//     classes.push(fullName);
//   }
//   res.send(classes);
// });

function convertNames(data) {
  var obj = data.body.classes;
  var classes = []
  for (let cls in obj) {
    cls = obj[cls];
    let department = mapping[cls.dept];
    if (!department) {
      console.log("ERROR: " + cls.dept + " is not a valid department name.");
    }
    let fullName = department + " " + cls.name;
    classes.push(fullName);
  }
  return classes;
}

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
