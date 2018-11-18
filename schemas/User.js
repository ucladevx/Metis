var mongoose = require('mongoose');
var Schema = mongoose.Schema;

// Format of User documents
var User = new Schema({
  id: {type: Number},
  name: {type: String},
  year: {type: String},
  start_term: {type: String},
  major: {type: String},
  minor: {type: String},
  interests: {type: String},  // TODO: figure out how to represent this
  classes: {type: [Number]},  // class_ids that they have taken
});

mongoose.model('User', User);

// TODO: host on mLab
// set up referential integrity
// create routes to query
