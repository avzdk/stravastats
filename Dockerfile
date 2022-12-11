FROM python:latest
COPY . .        
RUN pip install -r requirements.txt
WORKDIR ./myapp
CMD ["uwsgi","wsgi.ini"]
