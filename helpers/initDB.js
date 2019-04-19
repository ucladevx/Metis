//Art, Arts and Architecture, Civic Engagement, Dentistry, Disability Studies, Education, Family Medicine, Graduate Student Professional Development, International Migration Studies, Management, Medical History, Medicine, Music, Pediatrics, Public Affairs, Urology
//Asian am, c&ee, esl, latin am, pbmed
const express = require('express');
var router = express.Router();
const dbHelpers = require('../helpers/db.js');

const prereqJSON = require('../python/complete.json');

async function populatePrereqs(){

	const dbase = dbHelpers.getDb();
	const db = dbase.db("Metis");
	const prereqCollection = db.collection("Prerequisites")

	for(var major in prereqJSON){
		/* Not sure if needed
		if (!prereqJSON.hasOwnProperty(major)) {
        The current property is not a direct property of p
        	continue;
    	}
    	*/
    	majorClasses = prereqJSON[major];

		for(var classID in majorClasses){
	    	pathways = majorClasses[classID];
	    	var prereqEntry = {
	    		"class_id" : classID,
	    		"prerequisites": pathways
	    	}
			//console.log(prereqEntry);
			try {
				r = await prereqCollection.updateOne(
					{ "class_id" :  classID },
			        { $set: {"prerequisites": pathways} },
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

dbHelpers.initDb(function(err){
	populatePrereqs();
});
