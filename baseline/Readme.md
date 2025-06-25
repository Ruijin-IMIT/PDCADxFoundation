
## Baseline model and usage

### Download the source codes and models
Find the source codes at Ruijin-IMIT open-source platforms:

Github: https://github.com/Ruijin-IMIT/PDCADxFoundation/baseline

Gittee: https://gitee.com/ruijin-imit/PDCADxFoundation/baseline

Download the model weights:

Google Drive: https://drive.google.com/drive/folders/1EGzzLvoTE_IyfbT_S7bBfZFqMXAZkLFs?usp=sharing

Baidu Drive:  https://pan.baidu.com/s/1MNW8QS0FfvTnGUf_e3ad7Q?pwd=RJPD

### Environment setup & package installation
Requirement:

Hardware: CPU X86_64, GPU: Nvidia GPU, Memory: >= 32 GB

Operating system: Ubuntu >= 20.04

Python Version: > 3.10

Create a seperate python environment, and install dependencies:
```bash
python3 -m venv pdcad # create a virtual environment
source pdcad/bin/activate # activate pdcad env

cd xxx/PDCADxFoundation/baseline

cd nnUNet-2.6.0
pip install .   # install nnUNet to current env
cd ../RRMediCa 
pip install -r requirements.txt  # install RRMediCa dependencies
```

### Inference
Set up the testing paths and make predictions:
```bash
cd xxx/PDCADxFoundation/baseline
input_dir = xxx/test_input # val case dirs or test case dirs
output_dir = xxx/test_output # the final results: segment masks in each case folder, and the pred.csv for all PD cases
temp_dir = xxx/test_temp # intermediate results or temp files, may be used for convenience 
model_dir = xxx/models # directory containing the model weights/checkpoints
python baseline.py input_dir output_dir temp_dir model_dir

```

### Evaluation
The evaluation codes and process will be updated in the challenge website and Github repository. 



