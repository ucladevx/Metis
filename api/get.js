const express = require('express');
const mongoose = require('mongoose');
var router = express.Router();

// functions called by API endpoints
const requisiteHelpers = require('../helpers/checkRequisites.js');
const dbHelpers = require('../helpers/db.js');

router.get('/test/:name', (req,res  )=> {
  res.send("Welcome, " + req.params.name);
});

// create databases and collections
// use to reset db during dev, don't include in prod server
router.get('/initDB', function(req, res, next){

  const dbase = dbHelpers.getDb();

  const db1 = dbase.db("Scrape")
  db1.createCollection("Classes")

  const db2 = dbase.db("ML")
  db2.createCollection("Class_Clusters")

  const db3 = dbase.db("Metis")
  db3.createCollection("Users")

});

/*
router.get('/checkRequisites', function(req,res,next){
	const dbase = dbHelpers.getDb();
	const db = dbase.db("Metis");
	const prereqCollection = db.collection("Prerequisites");

	var initialState = req.body.student;
	var takenCourses = requisiteHelpers.parseTakenClasses(initialState);

	var targetCourse = req.body.target;
	var courseObject = await prereqCollection.findOne({'class_id': targetCourse});
	if (courseObject == null){
		res.status(404).json({
			'exists':false,
			'valid':false,
			'pathway':[]
		});
		return;
	}
	var coursePathways = courseObject.prerequisites;

	var validPathway = requisiteHelpers.checkReqs(coursePathways,takenCourses);
	if(validPathway == null)
		res.status(200).json({
			'exists':true,
			'valid':false,
			'pathway':[]
		})
	else
		res.status(200).json({
			'exists':true,
			'valid':true,
			'pathway':validPathway
		})
	return;
});
*/

router.get('/majors', async function(req,res,next){
	const dbase = dbHelpers.getDb();
	const db = dbase.db("Metis");
	const departments = db.collection("Departments");
	var majorList = [];

	try{
		var objectArray = await departments.find().toArray();
		for(var object of objectArray){
			majorList.push(object["department_id"]);
		}
		res.send(majorList);

	} catch(error){
		console.log(error);
		res.send(error);
	}

});

async function validClasses(major,takenCourses){
	const dbase = dbHelpers.getDb();
	const db = dbase.db("Metis");
	const courses = db.collection("Course");
	var validClasses = {};

	var objectArray = await courses.find({"department":major}).toArray();
	for(var courseObject of objectArray){
		var courseID = courseObject["class_id"];
		var coursePathways = courseObject["prerequisites"];
		//console.log(coursePathways);
		var checkedPathways = requisiteHelpers.checkPathways(takenCourses,coursePathways);

		validClasses[courseID] = checkedPathways;

		//validClasses[courseID] = 1;
	}
	console.log(validClasses);
};

// dbHelpers.initDb(function(err){
// 	validClasses("Computer Science",['Computer Science 31','Computer Science 32','Computer Science 33']);
// 	return;
// });


//parameter: array of class_ids taken
//route for old function of checking if user can take a certain class

//route for new function given major, what classes user can take from the pool. Returns json of all class names, true if can, list of classes to take that class if not. JSON of class_ids: {bool, [string]}
module.exports = router;
