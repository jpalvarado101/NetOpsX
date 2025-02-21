FROM node:16

WORKDIR /app

COPY package.json package-lock.json* ./
RUN npm install --unsafe-perm

# Ensure the binaries in node_modules/.bin are executable
RUN chmod -R 755 node_modules/.bin && chmod +x node_modules/.bin/react-scripts

COPY . .

EXPOSE 3000

CMD ["npm", "start"]
