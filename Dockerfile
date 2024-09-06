FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

RUN apt-get update && apt-get install -y \
    build-essential \
    libatlas-base-dev

# Copier les traductions
COPY locales .

# Copier le main
COPY app.py .

# Copier les modules
COPY create_rfi.py .
COPY manage_rfi.py .
COPY send_rfi.py .
COPY settings.py .
COPY update_rfi.py .

# Copier CRUD
COPY create.py .
COPY read.py .
COPY update.py .

# Copier le generateur de xslx
COPY generateXlsx.py .

# Copier le connecteur NextCloud
COPY nextcloud.py .

# Copier les fonctions utils
COPY utils.py .

# Copier le fichier de conf streamlit-auth
RUN mkdir -p /app/auth/
COPY auth/cred.yaml auth/cred.yaml 

## COPY set configuration

# Expose the Streamlit default port
EXPOSE 8501

# Set environment variables for Streamlit
ENV STREAMLIT_PORT=8501
ENV PYTHONPATH=.:$PYTHONPATH

# Run the Streamlit app
CMD ["streamlit", "run", "app.py"]
