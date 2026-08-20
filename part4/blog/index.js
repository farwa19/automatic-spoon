const config = require('./utils/config')

const { info, error } = require('./utils/logger')
const app = require('./app') 

const PORT = 3002
app.listen(config.PORT, () => {
  console.log(`Server runing on port ${PORT}`)
})