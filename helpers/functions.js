var clusters = require('../python/clustering/clusters.json');

// acronym mapping
const mapping = require('../utils/acronym_mapping.json')

var classStringMap = {
  "COM SCI" : "Computer Science",
  "PHYS" : "Physics",
  "MATH" : "Mathematics",
  "KOREA" : "Korean"
};

function hello(){
  return "Hello";
}

function findRecommended(classesTaken){
  var recommendations = [];
  for (var i = 0; i < classesTaken.classes.length; i++)
  {
    for (var j = 0; j < classesTaken.classes[i].length; j++)
    {
      var rec = new Object();
      rec.class_taken = classesTaken.classes[i][j];
      var deptRecs = clusters[classStringMap[rec.class_taken.dept]]
      var found = false;
      for (var k = 0; !found && deptRecs["lowerdiv"] && k < deptRecs["lowerdiv"].length; k++)
      {
        var cluster = deptRecs["lowerdiv"][k];
        if (cluster.includes(rec.class_taken.name))
        {
          rec.similar_classes = cluster.filter((value) => value != rec.class_taken.name);
          found = true;
        }
      }
      for (var k = 0; !found && deptRecs["upperdiv"] && k < deptRecs["upperdiv"].length; k++)
      {
        var cluster = deptRecs["upperdiv"][k];
        if (cluster.includes(rec.class_taken.name))
        {
          rec.similar_classes = cluster.filter((value) => value != rec.class_taken.name);
          found = true;
        }
      }
      for (var k = 0; !found && deptRecs["grad"] && k < deptRecs["grad"].length; k++)
      {
        var cluster = deptRecs["grad"][k];
        if (cluster.includes(rec.class_taken.name))
        {
          rec.similar_classes = cluster.filter((value) => value != rec.class_taken.name);
          found = true;
        }
      }
      recommendations.push(rec);
    }
  }
  return recommendations;
}

function convertNames(data) {
  var obj = data.classes;
  var classes = []
  for (let q in data.quarters){
    if(q != 'search'){
      var cls_list = data.quarters[q].classIds

      for(var i = 0; i < cls_list.length; i++){
        var cls_id = cls_list[i]
        var cls = data.classes[cls_id];

        let department = mapping[cls.dept];
        if (!department) {
          console.log("ERROR: " + cls.dept + " is not a valid department name.");
        }
        let fullName = department + " " + cls.name;
        classes.push(fullName);

      }
    }

  }

  console.log(classes)
  return classes;
}


module.exports = {hello, findRecommended, convertNames}
