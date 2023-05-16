

RUN mkdir /app
WORKDIR /app

COPY main.py /app/main.py

ENTRYPOINT [ "dockerentrypoint" ]
CMD [ "/app/main.py" ]
