# Official Docker reference
Docker installation:
https://docs.docker.com/engine/install/ubuntu/#prerequisites


# Docker installation (using the Chinese source if needed)

Host operating system: Ubuntu 24.04 LTS.

## Install Docker using Chinese sources
If you encounter network problems while downloading resources from Docker official website, 
it is better to switch to a Chinese source (i.e. tsinghua, aliyun) for a smooth experience.

Use tsinghua source:
```bash
sudo apt-get update
sudo apt-get install ca-certificates curl gnupg lsb-release
curl -fsSL https://mirrors.tuna.tsinghua.edu.cn/docker-ce/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://mirrors.tuna.tsinghua.edu.cn/docker-ce/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

```
Use aliyun source:
```bash
sudo apt-get update
sudo apt-get install ca-certificates curl gnupg lsb-release
curl -fsSL http://mirrors.aliyun.com/docker-ce/linux/ubuntu/gpg | sudo apt-key add -
sudo sh -c 'echo "deb [arch=amd64] http://mirrors.aliyun.com/docker-ce/linux/ubuntu $(lsb_release -cs) stable" > /etc/apt/sources.list.d/docker.list'
```

Then install Docker:
```bash
sudo apt-get update
sudo apt-get install docker-ce docker-ce-cli containerd.io

# test if docker installation is OK
sudo systemctl status docker
docker --version
```
If any error occurs in the middle, solve it accordingly before proceeding.

Update (or create) the Docker config file: `vi /etc/docker/daemon.json`
```json
{
    "registry-mirrors": [
        "https://dockerproxy.com",
        "https://docker.m.daocloud.io",
        "https://cr.console.aliyun.com",
        "https://ccr.ccs.tencentyun.com",
        "https://hub-mirror.c.163.com",
        "https://mirror.baidubce.com",
        "https://docker.nju.edu.cn",
        "https://docker.mirrors.sjtug.sjtu.edu.cn",
        "https://github.com/ustclug/mirrorrequest",
        "https://registry.docker-cn.com"
    ]
}
```

```bash
# Reload the config file, then restart the docker:
sudo systemctl daemon-reload
sudo systemctl restart docker
# Check if Registry Mirrors are fine:
sudo docker info 
```

## Other resources (better connection if needed)
### Docker images
Browse the https://docker.aityp.com, you can find Docker images and downloading instructions. For example,
Nvidia CUDA images:
https://docker.aityp.com/r/docker.io/nvidia/cuda

Ubuntu Images:
https://docker.aityp.com/image/docker.io/ubuntu:latest

Docker CMD: docker pull swr.cn-north-4.myhuaweicloud.com/ddn-k8s/docker.io/ubuntu:latest


### Anaconda
Alternative downloading sites (version > 3-5.1, Linux, x86_64):
https://mirrors.tuna.tsinghua.edu.cn/anaconda/archive/?C=M&O=D

### Python/Pip
Change to a faster python/pip source:
```bash
pip install pip -U2 
pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
```

### Some commended Docker images:

[//]: # (pytorch installed with conda environment, development &#40;13GB&#41;:)

[//]: # (```bash)

[//]: # (docker pull swr.cn-north-4.myhuaweicloud.com/ddn-k8s/docker.io/pytorch/pytorch:2.6.0-cuda12.6-cudnn9-devel)

[//]: # (docker tag  swr.cn-north-4.myhuaweicloud.com/ddn-k8s/docker.io/pytorch/pytorch:2.6.0-cuda12.6-cudnn9-devel  docker.io/pytorch/pytorch:2.6.0-cuda12.6-cudnn9-devel)

[//]: # (```)
Pytorch installed with Conda environment (6GB):
```bash
docker pull swr.cn-north-4.myhuaweicloud.com/ddn-k8s/docker.io/pytorch/pytorch:2.6.0-cuda12.4-cudnn9-runtime
docker tag  swr.cn-north-4.myhuaweicloud.com/ddn-k8s/docker.io/pytorch/pytorch:2.6.0-cuda12.4-cudnn9-runtime  docker.io/pytorch/pytorch:2.6.0-cuda12.4-cudnn9-runtime
```
Ubuntu:24.10 (80MB):
```bash
docker pull swr.cn-north-4.myhuaweicloud.com/ddn-k8s/docker.io/ubuntu:24.10
docker tag  swr.cn-north-4.myhuaweicloud.com/ddn-k8s/docker.io/ubuntu:24.10  docker.io/ubuntu:24.10
```



