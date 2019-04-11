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
        { $set: {name: req.body.name} },
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
