FROM node:alpine
EXPOSE 7878

COPY . /app

WORKDIR /app

# Install packages
RUN npm i

# Build website
RUN npm run build

# Start next.js
CMD [ "npm", "start" ]