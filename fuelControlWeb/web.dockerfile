FROM python:3

WORKDIR /usr/src/app

COPY ./fuelControlWeb/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY ./fuelControlWeb .

CMD [ "python", "./runWeb.py" ]