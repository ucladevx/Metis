const express = require('express');
const mongoose = require('mongoose');
var router = express.Router();

const dbHelpers = require('../helpers/db.js')

/********* Schemas **********/

require('../schemas/User');
const userSchema = mongoose.model('User');

/********* End Schemas **********/

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

const maxClasses = {
	classes: [
    [
      { id: 1, dept: "COM SCI", name: "1" },
      { id: 2, dept: "COM SCI", name: "31" },
      { id: 3, dept: "KOREA", name: "50" },
      { id: 4, dept: "COM SCI", name: "M51A" }
    ],
    [
      { id: 5, dept: "COM SCI", name: "32" },
      { id: 6, dept: "COM SCI", name: "35L" },
      { id: 7, dept: "MATH", name: "33B" },
      { id: 8, dept: "PHYS", name: "1B" }
    ],
	]
}

router.post('/find-recommended', function(req, res, next) {
  var ans = helpers.findRecommended(maxClasses);
  res.send(ans);
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

// POST a User schema
router.post('/user', function(req, res, next){

  // get collection
  const dbase = dbHelpers.getDb();
  const db = dbase.db("Metis");
  const userDB = db.collection("Users")

  /*
    If req.body exists in Metis.Users collection,
      update document if there are changes
    Else
      insert new document to collection
  */
  try {
     userDB.updateOne(
        { id :  req.body.id },
        { $set: {
                name: req.body.name, 
                email: req.body.email, 
                major: req.body.major,
                startTerm: req.body.startTerm,
                takenCourses: req.body.takenCourses

              } 
        },
        { upsert: true }
     ).then((r) => {
       if(r["upsertedId"]){
         res.send("Created User document");
       }
       else if(r["modifiedCount"] > 0){
         res.send("Updated User document");
       }
       else{
         res.send("User document found but not updated");
       }
     });
  } catch (e) {
     print(e);
     res.send("Error inserting User document")
  }
});

module.exports = router;
