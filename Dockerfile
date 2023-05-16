ARG BASEIMAGE="python:3.10"

FROM kushmlcontainer.azurecr.io/base/${BASEIMAGE}

WORKDIR /app

COPY main.py /app/main.py

ENTRYPOINT [ "dockerentrypoint" ]
CMD [ "/app/main.py" ]
