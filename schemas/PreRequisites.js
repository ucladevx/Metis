var mongoose = require('mongoose');
var Schema = mongoose.Schema;

// Associate list of uppder div class_ids with a major
var PreRequisites = new Schema({
	"class_id" : {type: String},
	"prerequisites": {type: [[String]]}
});

module.exports = mongoose.model('PreRequisites', PreRequisites);
