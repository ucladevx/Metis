let {PythonShell} = require('python-shell')

function registrar(req, res) {
  PythonShell.run('../python/registrar.py', function (err, data) {
    if (err) res.send(err);
    else res.send(data.toString())
  });
}

module.exports = {registrar}
