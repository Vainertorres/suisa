#imagen base
FROM --platform=linux/amd64 python:3.11-slim-bullseye

#Setear variables de entorno
ENV PIP_DISABLE_PIP_VERSION_CHECK 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1


#Setear directorio de trabajo
WORkDIR /code

#Instalar dependencias
COPY ./Requirements.txt ./
RUN pip install -r Requirements.txt

##RUN apk update \
##    && apk add --no-cache gcc musl-dev postgresql-dev python3-dev libffi-dev \
##    && pip install --upgrade pip


#Copiar el proyecto
COPY . .

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]