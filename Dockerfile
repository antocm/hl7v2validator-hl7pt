FROM python:3.10-slim



# Install dependencies
RUN mkdir /app
WORKDIR /app
#COPY requirements.txt /app
#RUN pip install -r requirements.txt

RUN mkdir /app/hl7validator
COPY hl7validator /app/message_validatihl7validatoron_logger

RUN python3 -m pip install pip --upgrade
RUN python3 -m pip install --upgrade wheel setuptools

COPY requirements.txt /app
COPY run.py /app
COPY gunicorn.sh /app


RUN pip install -r requirements.txt
#RUN unzip model.zip 

EXPOSE 80
#CMD python run.py
RUN ["chmod", "+x", "./gunicorn.sh"]

ENTRYPOINT ["./gunicorn.sh"]