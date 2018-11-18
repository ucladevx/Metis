var mongoose = require('mongoose');
var Schema = mongoose.Schema;

// Associate list of uppder div class_ids with a major
var UpperDivs = new Schema({
  major_id: {type: Number},
  class_id: {type: [Number]},
});

mongoose.model('UpperDivs', UpperDivs);
