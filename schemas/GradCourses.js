var mongoose = require('mongoose');
var Schema = mongoose.Schema;

// Associate list of grad course class_ids with a major
var GradCourses = new Schema({
  major_id: {type: Number},
  class_id: {type: [Number]},
});

mongoose.model('GradCourses', GradCourses);
