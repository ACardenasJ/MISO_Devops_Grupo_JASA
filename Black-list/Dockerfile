FROM python:3.10.8
RUN mkdir -p /app_user_management
WORKDIR /app_user_management
ENV FLASK_APP app.py
ENV FLASK_RUN_HOST 0.0.0.0
EXPOSE 3000
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY . .
CMD [ "flask", "run","-p","3000"]