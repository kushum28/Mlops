FROM c94ba0ce52584150be713f692b7250d4.azurecr.io/base/python:3.10

RUN mkdir /app
WORKDIR /app
COPY src/Pat_Cain_Data.csv /app/train.py
COPY src/train.py /app/train.py
ENTRYPOINT [ "dockerentrypoint" ]
CMD [ "/app/train.py" ]