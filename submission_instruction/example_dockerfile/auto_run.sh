
# /auto_run.sh  is the entry point of your submitted docker image [Called by default]
# It should 1) copy model dependency files and setup the environment variables
#           2）Check /pdcad/inputs for testing cases
#           3) Infer with your model, and store predictions in /pdcad/outputs

#  ------------  Below is an example  ----------------  #
## Copy my conda env to a desired place
# /pdcad_env

# create a similar anaconda directory in the docker image
# Set up the PATH variable, try to put everything in the same path as it is in the developing host.
# This would ensure a smooth migration of code bases.
mkdir -p /home/wfk/anaconda/envs/
# create a softlink for pdcad python env, costing no extra space or time
ln -s /pdcad_env/pdcad_conda /home/wfk/anaconda/envs/pdcad
export PATH=$PATH:/home/wfk/anaconda/envs/pdcad

# Set up the nnUNet env [for illustration only]
export nnUNet_raw="/pdcad_env/nnunet/nnUNet_raw"
export nnUNet_preprocessed="/pdcad_env/nnunet/nnUNet_preprocessed"
export nnUNet_results="/pdcad_env/nnunet/nnUNet_results"

# you can call a python script, to conduct the pdcad logics, i.e. check inputs, do inference, save predictions.
python /pdcad_env/predict.py



# The final output folder should be like:
# /pdcad/outputs/RJPD_003 --|
#                           |---NM_pred.nii.gz 
#                           |---QSM_pred.nii.gz
#                           |---PD_pred.txt      # content: 0 or 1
# /pdcad/outputs/RJPD_007 --|
#                           |---NM_pred.nii.gz
#                           |---QSM_pred.nii.gz
#                           |---PD_pred.txt      # content: 0 or 1
