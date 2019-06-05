function convertFormat(classList){
	var output = {};
	var classes = {};
	var idArray = [];
	var id = 1;
	for (var courseName of classList){
		var idObject = {};
		var cid = "c" + id.toString();
		idArray.push(cid);
		id +=1;
		var arr = courseName.split(" ");
		var number = arr[arr.length-1];
		var dept = arr.splice(0,arr.length-1).join(" ");
		idObject = {"id":cid, "dept": dept, "name":number};
		classes[cid] = idObject;
	}

	var search = {"id":"search","title": "temporary", "classIds": idArray};
	output.search = search;
	output.classes = classes;

	return output
};

module.exports = {convertFormat};