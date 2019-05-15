//Art, Arts and Architecture, Civic Engagement, Dentistry, Disability Studies, Education, Family Medicine, Graduate Student Professional Development, International Migration Studies, Management, Medical History, Medicine, Music, Pediatrics, Public Affairs, Urology
//Asian am, c&ee, esl, latin am, pbmed
const express = require('express');
var router = express.Router();
const dbHelpers = require('../helpers/db.js');
const major_acronyms = require('../python/major_acronyms.json');
const clustersJSON = require('../python/clustering/clusters.json');

const prereqJSON = require('../python/complete.json');
const departmentsJSON = require("../python/major_list.json");
const acronymsJSON = require("../python/major_acronyms.json");


async function populateCourses(){

	const dbase = dbHelpers.getDb();
	const db = dbase.db("Metis");
	const courseCollection = db.collection("Course");

	for(var major in prereqJSON){

    	majorClasses = prereqJSON[major];

		for(var classID in majorClasses){

			var pathways = majorClasses[classID];
			var department = "";
			var similarClasses = [];
			var type = "";
			var departmentPattern = /([ a-zA-Z]*) [a-zA-Z]*[0-9]/g;

			try{
				var abbreviation = departmentPattern.exec(classID)[1];
				department = major_acronyms[abbreviation];

				var typePattern = /([0-9]+)/g;
				var number = typePattern.exec(classID)[1];
				
				if(parseInt(number) <100 ){
					type = "lower";
				}
				else if(parseInt(number)<200)
					type = "upper";
				else
					type = "grad";
				
		    	var similarClasses = []
		    	var similarType = type;
		    	if (similarType == "lower" || similarType =="upper")
		    		similarType += "div";

		    	var similarPattern = /[a-zA-z]+ ([a-zA-Z]*[0-9]+[a-zA-Z]*)/g
		    	var similarMatch = similarPattern.exec(classID)[1];

		    	var clusters = clustersJSON[department][similarType];
		    	var flag = false;
		    	for(var cluster of clusters){
		    		for(var item of cluster){
		    			//console.log(item)
		    			if(item == similarMatch){
		    				for(var similarItem of cluster){
		    					if(similarItem == similarMatch)
		    						continue;
		    					similarClasses.push(similarItem);
		    				}
		    				flag=true;
		    			}
		    			if(flag)
		    				break;
		    		}
		    		if(flag)
		    			break;
		    	}


			}catch(e)
			{
				department = "Error";
				similarClasses = [];
				type = "Error";
			}
			var courseEntry = {
		    		"class_id" : classID,
		    		"prerequisites": pathways,
		    		"department": department,
		    		"professor-term": "placeholder",
		    		"similar_classes": similarClasses,
		    		"type": type
		    	}
	    	//console.log(courseEntry);
			//console.log(prereqEntry);
			
			try {
				r = await courseCollection.updateOne(
					{ "class_id" :  classID },
			        { $set: {"prerequisites": pathways, "department": department, "professor-term": "placeholder", "similar_classes": similarClasses, "type": type} },
			        { upsert: true }
			       );
				if(r["upsertedId"]){
					console.log("Created User document " + classID);
				}
				else if(r["modifiedCount"] > 0){
					console.log("Updated User document " +  classID);
				}
				else{
					console.log("User document found but not updated " + classID);
				}
			} catch(e){
				console.log(e);
			}
			



		}
	}
	return null;
};


async function createDepartments(){
	const dbase = dbHelpers.getDb();
	const db = dbase.db("Metis");
	const departmentsCollection = db.collection("Departments");

	for(var major of departmentsJSON["majors"]){
		console.log(major);

		try {
			r = await departmentsCollection.updateOne(
				{ "department_id" : major  },
				{ $set: {"department_id": major}},
		        { upsert: true }
		       );
			if(r["upsertedId"]){
				console.log("Created User document " + major);
			}
			else if(r["modifiedCount"] > 0){
				console.log("Updated User document " +  major);
			}
			else{
				console.log("User document found but not updated " + major);
			}
		}
		catch(e){
			console.log(e);
		}

	}
}


//Course Acronymps

async function createAcronymsMap(){
    const dbase = dbHelpers.getDb();
	const db = dbase.db("Metis");
	const acronymsToMajorCollection = db.collection("AcronymsToMajor");
	const majorToAcronymsCollection = db.collection("MajorToAcronyms");

	for(var acronym in acronymsJSON){
		var major = acronymsJSON[acronym];

		try {
			r = await acronymsToMajorCollection.updateOne(
				{ "acronym" : acronym  },
				{ $set: {"major": major}},
		        { upsert: true }
		       );
			if(r["upsertedId"]){
				console.log("Created User document " + acronym);
			}
			else if(r["modifiedCount"] > 0){
				console.log("Updated User document " +  acronym);
			}
			else{
				console.log("User document found but not updated " + acronym);
			}
		}
		catch(e){
			console.log(e);
		}


		try {
			r = await majorToAcronymsCollection.updateOne(
				{ "major" : major  },
				{ $set: {"acronym": acronym}},
		        { upsert: true }
		       );
			if(r["upsertedId"]){
				console.log("Created User document " + major);
			}
			else if(r["modifiedCount"] > 0){
				console.log("Updated User document " +  major);
			}
			else{
				console.log("User document found but not updated " + major);
			}
		}
		catch(e){
			console.log(e);
		}


	}
}

dbHelpers.initDb(function(err){
	createAcronymsMap();
});

//createDepartments();