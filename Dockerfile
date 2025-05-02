# Use official Nginx image
FROM nginx:alpine

# Set working directory
WORKDIR /usr/share/nginx/html

# Remove default static files
RUN rm -rf ./*

# Copy static files into Nginx's public directory
COPY index.html .
COPY css/ ./css/
COPY js/ ./js/

# Expose port (not strictly necessary but good practice)
EXPOSE 80
