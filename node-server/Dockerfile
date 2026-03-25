# 1. Usamos una imagen ligera de Node.js
FROM node:18-slim

# 2. Directorio dentro del contenedor
WORKDIR /app

# 3. Copiamos los archivos de dependencias
COPY package*.json ./

# 4. Instalamos las librerías de Node
RUN npm install

# 5. Copiamos el resto del código del servidor
COPY . .

# 6. Exponemos el puerto que usa Express
EXPOSE 3000

# 7. Arrancamos la aplicación
CMD ["node", "app.js"]