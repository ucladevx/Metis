const express = require('express');
var router = express.Router();
const acronymMap = require('../python/major_acronyms');

function checkReqs(pathways,takenCourses){
	if(pathways.length==0)
		return []

	var totalReqs = {};
	//Initialize a mapping of all courses in pathways
	for(var pathway of pathways){
		for(var course of pathway){
			totalReqs[course] = false;
		}
	}

	//Mark true the interesecting courses into totalReqs mapping
	for(var course of takenCourses){
		if(course in totalReqs){
			totalReqs[course]=true;
		}
	}

	//Check if any pathway is fully satisfied
	for(var pathway of pathways){
		for(var course of pathway){
			if(totalReqs[course]==false)
				break;
			if(course==pathway[pathway.length-1])
				return pathway;
		}
		continue;
	}
	return null;
}

function parseTakenClasses(classesJSON){
	let quarters = classesJSON['classes'];
	let takenCourses = [];
	for(var quarter of quarters){
		for(var classJSON of quarter){
			takenCourses.push(acronymMap[classJSON.dept] + " " + classJSON.name);	
		}
	}
	return takenCourses;
}

//var takenCourses = parseTakenClasses(initialState);
//console.log(checkReqs([['Computer Science 1']],takenCourses));