const express = require('express');
var router = express.Router();

// functions called by API endpoints
const helpers = require('../helpers/scraper');

// TODO: not working!
router.get('/registrar/', helpers.registrar);

module.exports = router;
