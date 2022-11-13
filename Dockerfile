FROM python:3.9.4-slim
# set work directory
WORKDIR /src/app

# set env variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
COPY src/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# copy project
COPY . .