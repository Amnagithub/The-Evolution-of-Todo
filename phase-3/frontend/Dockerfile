FROM nginx:alpine

# Copy static export files
COPY out /usr/share/nginx/html

# Copy nginx configuration
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 7860

CMD ["nginx", "-g", "daemon off;"]
