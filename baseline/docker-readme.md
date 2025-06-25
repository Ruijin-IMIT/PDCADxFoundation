
## PDCAD sample docker image
Purpose: help participant to understand the basic testing and evaluation procedures. We provide a sample docker image 
containing a baseline implementation of both PDCAD challenge tasks. The PD classification accuracy of this baseline model
reach 63% on the validation set (100 cases) and 62% on the testing set (200 cases).

You can follow the instructions here for docker image creation and model testing.

### Docker Installation: 

Hardware: NVidia GPU memory >= 12 GB, host memory > 32 GB

Operating system: Ubuntu 24.04

1) install Docker:
you can either follow the Docker official website, or try the following steps:

```bash
sudo apt update
curl -fsSL https://get.docker.com | sudo sh
```
2) install NVIDIA container Tookit:
* Add repository and GPG key:
```bash
curl -fsSL https://nvidia.github.io/libnvidia-container/gpgkey | sudo gpg --dearmor -o /usr/share/keyrings/nvidia-container-toolkit-keyring.gpg
curl -s -L https://nvidia.github.io/libnvidia-container/stable/deb/nvidia-container-toolkit.list | sed 's#deb https://#deb [signed-by=/usr/share/keyrings/nvidia-container-toolkit-keyring.gpg] https://#g' | sudo tee /etc/apt/sources.list.d/nvidia-container-toolkit.list
```
* Update, install, config:
```bash
sudo apt update
sudo apt install -y nvidia-container-toolkit
sudo nvidia-ctk runtime configure --runtime=docker
sudo systemctl restart docker
```

Add current user to the docker group:
```bash
sudo groupadd docker
sudo usermod -aG docker $USER
newgrp docker
```

### Download the PDCAD baseline docker image, and test

1) Download links:
* Google Drive: https://drive.google.com/drive/folders/1EGzzLvoTE_IyfbT_S7bBfZFqMXAZkLFs?usp=sharing
* Baidu Drive: https://pan.baidu.com/s/1MNW8QS0FfvTnGUf_e3ad7Q?pwd=RJPD

   
2) Use pdcad:baseline1 image
You can try the baseline1 image, and check the testing procedures and result formats. 
**The output folder contains segmentation masks and PD classification csv results, 
your model outputs should follow similar file structures**

```bash
docker load -i pdcad_baseline1_docker_image.tar
docker images
# attach host volume to docker container:  /your/host/project/dir/docker-data should contain testing input folder
docker run --gpus all -it -v /your/host/project/dir/docker-data:/docker-data -m 64g --cpus 24 --shm-size 30g IMAGE-ID bash

## after login the baseline image, try to run the inference:
cd /workspace/baseline
python baseline.py /docker-data/test1/ /docker-data/output1/ /docker-data/temp1/ ./models/
# the inference results are saved in /your/host/project/dir/docker-data/output1/ 
# and your own model implementation should follow this manner (file structures)
```



### Create your own docker image
1) Create through live interaction
* Download the base PyTorch image
```bash
## Download the docker.io/pytorch/pytorch:2.6.0-cuda12.4-cudnn9-runtime from Docker Hub, or from a 3rd-party cloud
docker pull swr.cn-north-4.myhuaweicloud.com/ddn-k8s/docker.io/pytorch/pytorch:2.6.0-cuda12.4-cudnn9-runtime
docker tag  swr.cn-north-4.myhuaweicloud.com/ddn-k8s/docker.io/pytorch/pytorch:2.6.0-cuda12.4-cudnn9-runtime  docker.io/pytorch/pytorch:2.6.0-cuda12.4-cudnn9-runtime

docker run --gpus all -it -v /your/host/project/dir/docker-data:/docker-data -m 64g --cpus 24 --shm-size 30g IMAGE-ID bash
```


* After login the docker image, do some preparation if necessary 
```bash
chmod 1777 /tmp  # change the /tmp permission for apt function
apt update
apt install nano
apt install vim
# change the apt source if necessary: 
# cp /etc/apt/sources.list /etc/apt/sources.list.bak
# change the apt source if necessary: https://mirrors.tuna.tsinghua.edu.cn/help/ubuntu/
# change the pip source if necessary: https://mirrors.tuna.tsinghua.edu.cn/help/pypi/
# pip config set global.index-url https://mirrors.tuna.tsinghua.edu.cn/pypi/web/simple

```

* Now install your model/code solution into the docker container:
```bash
# copy your project codes, models into current running docker container
# xxx ... ...

# install project dependencies, for python project, or running environment
# pip install xxx
# apt install xxx 
## install necessary libs, for example for opencv-python:
# apt install libgl1
# apt install libglib2.0-0


# After successfully installing codes & dependencies, do the testing and make sure the model can predict correctly ...

```

* Now consolidate the container to a transferable image:

```bash
docker commit container_id pdcad_xxx_image:latest

docker save -o pdcad_xxx_team.tar pdcad_xxx_image:latest

# Remember to test your docker image on another machine
docker load -i pdcad_xxx_team.tar
docker run --gpus all -it -v /your/host/project/dir/docker-data:/docker-data -m 64g --cpus 24 --shm-size 30g IMAGE-ID bash
# run the test, make sure that results are saved to /your/host/project/dir/docker-data/output

```
2) create docker image by Dockerfile

Another way to creat a docker image is through the Dockerfile. You can search and try it out.







