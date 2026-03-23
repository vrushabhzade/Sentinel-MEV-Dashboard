# Use the official lightweight Python image.
FROM python:3.11-slim

# Set environment variables
ENV PYTHONUNBUFFERED=True
ENV PORT=8080
ENV APP_HOME=/app

# Create and set the working directory
WORKDIR $APP_HOME

# Copy the requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application into the container
COPY . .

# Open the port for Cloud Run
EXPOSE 8080

# Run the FastAPI server natively to serve backend data 
# (You can also change this to run streamlit via: CMD ["streamlit", "run", "dashboard/app.py", "--server.port=8080", "--server.address=0.0.0.0"])
CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8080"]
