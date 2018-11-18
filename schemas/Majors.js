var mongoose = require('mongoose');
var Schema = mongoose.Schema;

// Store Information for a given Major
var Majors = new Schema({
  major_id: {type: Number},
  major_name: {type: String},
  required_classes: {type: [Number]}   // list of required class_ids
});

mongoose.model('Majors', Majors);
