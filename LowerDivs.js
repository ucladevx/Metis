var mongoose = require('mongoose');
var Schema = mongoose.Schema;

// Associate list of lower div class_ids with a major
var LowerDivs = new Schema({
  major_id: {type: Number},
  class_id: {type: [Number]},
});

mongoose.model('LowerDivs', LowerDivs);
