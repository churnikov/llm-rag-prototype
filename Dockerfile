FROM deepset/hayhooks:main

COPY /src/pipelines /opt/pipelines

#USER $USER

EXPOSE 8000

#ENV PATH="/opt/venv/bin:$PATH"

CMD ["hayhooks", "run", "--host", "0.0.0.0", "--port", "8000"]
