FROM python:3

WORKDIR /usr/src/app

COPY ./fuelControlDatabaseService/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY ./fuelControlDatabaseService .

CMD [ "python", "/fuelControlDatabaseService/runDatabaseService.py" ]