FROM deepset/hayhooks:main

COPY /src/pipelines /opt/pipelines

#USER $USER

EXPOSE 1416

#ENV PATH="/opt/venv/bin:$PATH"

#CMD ["hayhooks", "run", "--host", "0.0.0.0"]
