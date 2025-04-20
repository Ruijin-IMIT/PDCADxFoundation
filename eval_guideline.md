
# Model Submission 
## Docker image
To test the model performance, each participant team should pack the model into a Docker image.
The organizer will test the submitted solution in Ubuntu environment, with 80GB memory and one A5000 GPU.
Your docker solution should be tested in a similar environment before submission, Ubuntu 22-25 LTS, one NVIDIA GPU with memory small than 12 GB, 
The docker image size should not exceed 15GB, uses at most one CUDA GPU, requires at most 64 GB memory, spends at most 30 seconds on each testing case.


## Evaluation Description File
Please document the running record of your docker solution, to reduce misunderstanding and ease the communication.
Things to include:
1. your docker testing environment, host Linux version, docker version, GPU type.
2. The docker image: name, size, starting command, resource requirement.
3. The running result on the provided 5 eval cases.

Use screenshot as necessary.

## Submission methods
Please upload above materials to Baidu Drive, or Google Drive, and send us the download link through email.
Email title: Team [your team name]: validation submission
Email title: Team [your team name]: test submission

The organizer prefers the Baidu Drive due to a faster speed in China.



# Evaluation & Performance


## Metrics
Please refer to the metric.py script currently. We'll provide more details in May.

## Result feedback
We will send back the evaluation results through email.
If your submission failed, we will also notify you.

We will publish your evaluation result by default, on the PDCADxFoundation challenge website.


