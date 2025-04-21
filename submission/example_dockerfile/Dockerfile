# Start your image with a Ubuntu base image
# FROM swr.cn-north-4.myhuaweicloud.com/ddn-k8s/docker.io/ubuntu:24.10
FROM ubuntu:24.10

WORKDIR /

# Recommend: update your anaconda to Python > 3.11; create a new conda env for your pdcad models
# Put your anaconda environment under pdcad_env folder;
# Copy the python environment, to somewhere in the docker image
# Adjust the path & env variables in /auto_run.sh as needed
COPY pdcad_env /pdcad_env

# /auto_run.sh  is the entry point of your submitted docker image [Called by default]
# It should 1) copy model dependency files and setup the environment variables
#           2）Check /pdcad/inputs for testing cases
#           3) Infer with your model, and store predictions in /pdcad/outputs
COPY auto_run.sh /

# Start the app
CMD [ "bash", "auto_run.sh" ]












