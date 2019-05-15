const express = require('express');
var router = express.Router();
const acronymMap = require('../python/major_acronyms');
/*
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
}*/

function checkPathways(takenCourses, pathways){
	if(pathways.length == 0)
		return [];

	//var satisfiedFlag = 0;
	var incompletePathways = []; 

	for(var pathway of pathways){
		var checkedPathway = checkSinglePathway(takenCourses, pathway);

		if(checkedPathway.length == 0)
			return [];
		else
			incompletePathways.push(checkedPathway);
	}
	return incompletePathways;
};

function checkSinglePathway(takenCourses,pathway){
	var incompletePathway = [];
	for(var course of pathway){
		if(takenCourses.includes(course))
			continue;
		else
			incompletePathway.push(course);
	}
	return incompletePathway; //returns empty [] if pathway is satisfied
};
/*
function parseTakenClasses(classesJSON){
	let quarters = classesJSON['classes'];
	let takenCourses = [];
	for(var quarter of quarters){
		for(var classJSON of quarter){
			takenCourses.push(acronymMap[classJSON.dept] + " " + classJSON.name);	
		}
	}
	return takenCourses;
}*/

module.exports = {checkPathways};

//var takenCourses = parseTakenClasses(initialState);
//console.log(checkReqs([['Computer Science 1']],takenCourses));