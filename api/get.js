const express = require('express');
const mongoose = require('mongoose');
var router = express.Router();

// functions called by API endpoints
const requisiteHelpers = require('../helpers/checkRequisites.js');
const dbHelpers = require('../helpers/db.js');

const helperFunctions = require('../helpers/functions');
// const convertHelpers = require('../helpers/courseListToTiles');

// reverse major names mapping
const reverseMap = require('../utils/reverse_acronym_mapping')

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

/*
dbHelpers.initDb(function(err){
	search("Mathematics");
	return;
});
*/
module.exports = router;


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
