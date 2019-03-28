var mongoose = require('mongoose');
var Schema = mongoose.Schema;

var ClassObject = new Schema({
  id: Number,
  dept: String,
  name: String,
});

// Store Information for a given Major
var ClassList = new Schema({
  classes: {type: [[ClassObject]]}
});

module.exports = mongoose.model('ClassList', ClassList);
