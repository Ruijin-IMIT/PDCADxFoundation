


Your docker image would be run with cmd:

```bash
docker run  --gpus 1  --cpus 24  -m 64g  --shm-size 30g  -it  -v  /PDCAD/test_data:/pdcad  Image-ID  bash /auto_run.sh
```

The /pdcad/inputs structure is like:
```bash
# /pdcad/outputs/RJPD_003 --|
#                           |---NM.nii.gz 
#                           |---QSM.nii.gz
#                           |---T1.nii.gz
# /pdcad/outputs/RJPD_007 --|
#                           |---NM.nii.gz 
#                           |---QSM.nii.gz
#                           |---T1.nii.gz
# /pdcad/outputs/RJPD_xxx ... ...

```


The final output folder should be like:
```bash

# /pdcad/outputs/RJPD_003 --|
#                           |---NM_pred.nii.gz 
#                           |---QSM_pred.nii.gz
#                           |---PD_pred.txt      # content: 0 or 1
# /pdcad/outputs/RJPD_007 --|
#                           |---NM_pred.nii.gz
#                           |---QSM_pred.nii.gz
#                           |---PD_pred.txt      # content: 0 or 1


```















