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

// reverse major names mapping
const reverseMap = require('../utils/reverse_acronym_mapping')
const helperFunctions = require('../helpers/functions');
const convertHelpers = require('../helpers/courseListToTiles');
const requisiteHelpers = require('../helpers/checkRequisites.js');

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

// Given a department(full name), return tiles to display on frontend
/* Route parameter:
{
	"department": "Computer Science"
}
*/
router.post('/initDeptTiles', async function(req,res,next){

	const dbase = dbHelpers.getDb();
	const db = dbase.db("Metis");
	const courses = db.collection("Course");

	var department = req.body.department;

	var courseList = [];

	try{
		var objectArray = await courses.find({"department":department}).toArray();
  } catch(error){
		console.log(error);
	}
	for(var course of objectArray){
		courseList.push(course["class_id"]);
	}

	var returnObject = convertHelpers.convertFormat(courseList, 1, "");
	console.log(returnObject);
	res.send(returnObject);

});

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

// Given department and classes a user has taken, return recommended classes
/* Route Paramter
{
   "department":"Computer Science",
   "takenCourses":{
      "classes":{
         "c1":{
            "id":"c1",
            "dept":"COM SCI",
            "name":"1"
         },
         "c2":{
            "id":"c2",
            "dept":"COM SCI",
            "name":"31"
         },
         "c3":{
            "id":"c3",
            "dept":"ENGCOMP",
            "name":"3"
         },
         "c4":{
            "id":"c4",
            "dept":"MATH",
            "name":"31A"
         },
         "c5":{
            "id":"c5",
            "dept":"PHYSICS",
            "name":"1B"
         },
         "c6":{
            "id":"c6",
            "dept":"PHYSICS",
            "name":"1C"
         }
      },
      "quarters":{
         "search":{
            "id":"search",
            "title":"To Do",
            "classIds":[
               "c5",
               "c6"
            ]
         },
         "q1":{
            "id":"q1",
            "title":"To Do",
            "classIds":[
               "c1",
               "c2"
            ]
         },
         "q2":{
            "id":"q2",
            "title":"To Do",
            "classIds":[
               "c4"
            ]
         },
         "q3":{
            "id":"q3",
            "title":"To Do",
            "classIds":[

            ]
         },
         "q4":{
            "id":"q4",
            "title":"To Do",
            "classIds":[
               "c3"
            ]
         }
      },
      "quarterOrder":[
         "q1",
         "q2",
         "q3",
         "q4"
      ]
   }
}
*/

//expects "department" and "takenCourses" in req.body
router.post('/validMajorClasses', async function(req,res,next){

	const dbase = dbHelpers.getDb();
	const db = dbase.db("Metis");
	const courses = db.collection("Course");
	var validClasses = {};

	var major = req.body.department;
	var takenCourses = helperFunctions.convertNames(req.body.takenCourses);
	try{
		var objectArray = await courses.find({"department":major}).toArray();
	} catch(error){
		console.log(error);
		res.send(error);
	}

	var output = {};
	output.requirementsLeft = requisiteHelpers.validClasses(takenCourses,objectArray);

	let canTake = [];
	for (cls in output.requirementsLeft) {
		if (output.requirementsLeft[cls].length === 0)
			canTake.push(cls);
	}
	output.canTake = canTake;

	let canTakeUpdated = []
	for (cls in canTake) {
		cls = canTake[cls];
		let id = cls.split(" ");
		id = id[id.length - 1];
		id = id.replace(/[A-Z]/g, '');
		id = parseInt(id);
		if (id < 200)
			canTakeUpdated.push(cls);
	}

	var filteredClasses = canTakeUpdated;
	var recommendedClasses = [];
	var newTakenCourses = [];
  // console.log(takenCourses)
	for (cls in takenCourses) {
		cls = takenCourses[cls];
		let lastIndex = cls.lastIndexOf(" ");
		let dept = cls.substring(0, lastIndex);

		let deptConverted = reverseMap[dept];
		let id = cls.split(" ");
		id = id[id.length - 1];
		let finalName = deptConverted + " " + id;

		newTakenCourses.push(finalName);
	}

	var abbrevDept = newTakenCourses[0].split(" ");
	abbrevDept = abbrevDept.splice(0,abbrevDept.length - 1).join(" ");
	for(var course of newTakenCourses){

		try{
			var cluster = [];
			for(object of objectArray){
				if (object["class_id"]==course){
					cluster = object["similar_classes"];
				}

			}
			for (var clusterCourseNum of cluster){
				var clusterCourseName = abbrevDept + " " + clusterCourseNum;

				if (filteredClasses.includes(clusterCourseName) && !newTakenCourses.includes(clusterCourseName))
					recommendedClasses.push(clusterCourseName);
			}
		} catch (e){
			console.log(e);
		}
	}

	output.recommended = recommendedClasses;
	var classes_ML = convertHelpers.convertFormat(output.recommended, 1, "_ML");
  var classes_normal = convertHelpers.convertFormat(output.canTake, 1 + output.recommended.length, "");

  var returnObject = {
    "search": {
        "id": "search",
        "title": "temporary",
        "classIds": []
    },
    "classes": {
        "c1": {
            "id": "c1",
            "dept": "COM SCI",
            "name": "32"
        }
    }
  }

  for(var i = 0; i < classes_ML.search.classIds.length; i++){
    var currID = classes_ML.search.classIds[i];
    returnObject.search.classIds.push(currID + "_ML");
    returnObject.classes[currID + "_ML"] = classes_ML.classes[currID]
  }

  for(var i = 0; i < classes_normal.search.classIds.length; i++){
    var currID = classes_normal.search.classIds[i];
    returnObject.search.classIds.push(currID);
    returnObject.classes[currID] = classes_normal.classes[currID]
  }
	res.send(returnObject);
	return;

});

module.exports = router;
