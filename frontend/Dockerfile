FROM node:24.15-alpine AS build
WORKDIR /app

COPY package*.json ./
RUN npm install --no-audit --no-fund

COPY . .
RUN npm run build

FROM nginx:1.27-alpine AS production
COPY nginx/default.conf /tmp/default.conf
RUN sed -i "s|__PORT__|80|g; s|__FRONTEND_ROOT__|/usr/share/nginx/html|g" /tmp/default.conf && \
    cp /tmp/default.conf /etc/nginx/conf.d/default.conf
COPY --from=build /app/dist/temp-app/browser /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
