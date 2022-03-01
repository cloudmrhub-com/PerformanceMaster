FROM conda/conda-rpm-deb
LABEL maintainer="Dr. Eros Montin, PhD <eros.montin@gmail.com>"


#creating the apptmp
RUN mkdir /apptmp

RUN mkdir /celery_tasks

WORKDIR /celery_tasks


ADD https://api.github.com/repos/erosmontin/myPy/git/refs/heads/main version.json
RUN git clone https://github.com/erosmontin/myPy.git
#fixing neccessary packages
RUN conda env create -f myPy/environment.yml

#copy the code
COPY . /celery_tasks

#sign!
RUN mkdir /cloudmr/
RUN echo "Performance Master, \ built the " `date` "from user " $USER  >/cloudmr/buildversion.txt
ENTRYPOINT ["conda", "activate", "me"]