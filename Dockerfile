FROM flywheel/python:main.771cdc04
ENV FLYWHEEL="/flywheel/v0"
WORKDIR ${FLYWHEEL}

# Dev install. git for pip editable install.
USER root
RUN apt-get update &&  \
    apt-get install --no-install-recommends -y git && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# Installing main dependencies
COPY requirements.txt $FLYWHEEL/
RUN pip install --no-cache-dir -r $FLYWHEEL/requirements.txt

RUN pip install flywheel-gear-toolkit && \
    pip install flywheel-sdk
    
# Installing the current project (most likely to change, above layer can be cached)
COPY ./ $FLYWHEEL/
# RUN pip install --no-cache-dir .

# Configure entrypoint
RUN chmod a+x $FLYWHEEL/run.py
ENTRYPOINT ["python","/flywheel/v0/run.py"]
