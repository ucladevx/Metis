var mongoose = require('mongoose');
var Schema = mongoose.Schema;

// Data for a class
var Classes = new Schema({
  class_id: {type: Number},
  catalog_number: {type: String},
  course_name: {type: String},
  units: {type: String},
  description: {type: String},
  days: {type: String},
  time: {type: String},
  location: {type: String},
  units: {type: String},
  instructors: {type: String},
})

mongoose.model('Classes', Classes);
