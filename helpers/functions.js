
function hello(){
  return "Hello";
}

function findRecommended(classesTaken){
  var recommendations = [];
  for (var i = 0; i < classesTaken.length; i++)
  {
    for (var j = 0; j < classesTaken[i].length; i++)
    {
      var obj;
      obj.classTaken = classesTaken[i][j];
    }
  }

  return recommendations;
}

module.exports = {hello}
