FROM deepset/hayhooks:main

COPY /src/pipelines /opt/pipelines

COPY /src/start-script.sh start-script.sh

RUN chmod ug+x start-script.sh

EXPOSE 8000

CMD ["hayhooks", "run", "--host", "0.0.0.0", "--port", "8000"]
