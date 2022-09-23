FROM node:16

RUN mkdir /opt/app
WORKDIR /opt/app
COPY  package*.json ./
RUN npm install
COPY  . .

ENTRYPOINT [ "node", "app.js"]