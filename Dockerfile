FROM python:3.12.6
EXPOSE 5000
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
ENV FLASK_APP=app
ENV FLASK_ENV=development
CMD [ "flask","run","--host","0.0.0.0" ]

