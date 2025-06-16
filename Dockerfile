# Step 1: Use an official Nginx image to serve the frontend
FROM nginx:alpine

# Step 2: Copy the frontend files into the Nginx container
COPY ./frontend /usr/share/nginx/html

# Step 3: Expose the default port for Nginx (80)
EXPOSE 80

# Step 4: Run Nginx
CMD ["nginx", "-g", "daemon off;"]
