const key = require('./key')

module.exports = {
  db: {
    mongoURI: key,
    connectionOptions: { useNewUrlParser: true }
  }
}
