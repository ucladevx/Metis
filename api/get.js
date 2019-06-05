const express = require('express');
const mongoose = require('mongoose');
var router = express.Router();

// functions called by API endpoints
const requisiteHelpers = require('../helpers/checkRequisites.js');
const dbHelpers = require('../helpers/db.js');

const helperFunctions = require('../helpers/functions');
const convertHelpers = require('../helpers/courseListToTiles');

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
{
	"department": "Computer Science",
	"takenCourses": ["Computer Science 31","Computer Science 32","Computer Science 33"]
}
*/

//expects "department" and "takenCourses" in req.body
router.get('/validMajorClasses', async function(req,res,next){

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
		console.log(cls);
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
	console.log(newTakenCourses)
	console.log(filteredClasses)

	var abbrevDept = newTakenCourses[0].split(" ");
	abbrevDept = abbrevDept.splice(0,abbrevDept.length - 1).join(" ")
	console.log(abbrevDept)
	for(var course of newTakenCourses){

		try{
			var cluster = [];
			for(object of objectArray){
				if (object["class_id"]==course){
					cluster = object["similar_classes"];
					console.log(cluster);
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
	var returnObject = convertHelpers.convertFormat(output.recommended);
	//console.log(output);
	//res.status(200).json(output);
	res.send(returnObject);
	return;

});

/* Route parameter:
{
	"department": "Computer Science"
}
*/
router.get('/initDeptTiles', async function(req,res,next){

	const dbase = dbHelpers.getDb();
	const db = dbase.db("Metis");
	const courses = db.collection("Course");

	var department = req.body.department;

	var courseList = [];

	try{
		var objectArray = await courses.find({"department":department}).toArray();
	} catch(error){
		console.log(error);
		//res.send(error);
	}
	for(var course of objectArray){
		courseList.push(course["class_id"]);
	}
	//var returnObject = {"department": courseList};

	var returnObject = convertHelpers.convertFormat(courseList);
	console.log(returnObject);
	res.send(returnObject);

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



/*

REQUEST BODY for validMajorClasses

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