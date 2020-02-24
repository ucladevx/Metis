let {PythonShell} = require('python-shell')

//
// Attempting to run scrapers via routes, not working
// TODO: create microservices
//
function registrar(req, res) {
  PythonShell.run('../python/registrar.py', function (err, data) {
    if (err) res.send(err);
    else res.send(data.toString())
  });
}

module.exports = {registrar}
