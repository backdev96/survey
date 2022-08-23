FROM node:14 as build-stage

WORKDIR /app

# Install dependencies needed for build
# RUN apk add git python3 make g++ python2

ENV VITE_API_URL="http://localhost:8000/"
ENV BASE_PATH="/"

EXPOSE 8081

CMD npm install && npm run dev