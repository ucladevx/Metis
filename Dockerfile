FROM node:9.11.1-alpine

# Directory
ARG APP_DIR=app
RUN mkdir -p ${APP_DIR}
WORKDIR ${APP_DIR}

# TODO: idk what this does
ENV PATH /usr/src/node_modules/.bin:$PATH

# Install dependencies
COPY package*.json ./
RUN npm install

# Install nodemon
RUN npm install --global nodemon

# For production
# RUN npm install --production

# Copy project files
COPY . .

# Expose running port
EXPOSE 3000

# Run the project
CMD ["node", "index.js"]
# CMD ["nodemon","index.js"]
