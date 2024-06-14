FROM deepset/hayhooks:main

ENV USER=hhuser
ENV OPENAI_API_KEY=YOUR-API-KEY

RUN apt-get update && apt-get install -y vim

#RUN pip install --no-cache-dir --upgrade pip==23.3.2 \
#    && pip install --no-cache-dir "sentence-transformers>=2.2.0"

# Add user to system
RUN useradd -m -u 1000 $USER

COPY /src/pipelines /opt/pipelines

WORKDIR /opt/hayhooks

COPY /src/start-script.sh start-script.sh
COPY /src/.env.template .env

RUN chown -R $USER:$USER . && \
    chmod ug+x start-script.sh

USER $USER
EXPOSE 8000

#CMD ["hayhooks", "run", "--host", "0.0.0.0", "--port", "8000"]

ENTRYPOINT ["./start-script.sh"]
