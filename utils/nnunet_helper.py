
import os
import shutil
# import numpy as np
import copy

'''
Make sure the predicted masks are copied into case folders by casename in pdcad output dir.
Each predicted mask should be named as MOD_pred.nii.gz, MOD can be 'NM' or 'QSM'.
The automatic evaluating process will depend on this storing convention.

'''

def copy_preds_to_outputs(mr_mod, nnunet_pred_dir, pdcad_output_dir):
    preds = os.listdir(nnunet_pred_dir)
    preds = [p for p in preds if '.nii.gz' in p]
    casenames = [p.split('.nii.gz')[0] for p in preds]
    for c in casenames:
        dst_dir = os.path.join(pdcad_output_dir, c)
        if not os.path.exists(dst_dir):
            os.mkdir(dst_dir)
        src = os.path.join(nnunet_pred_dir, c + '.nii.gz')
        dst = os.path.join(dst_dir, mr_mod + '_pred.nii.gz')
        shutil.copy(src, dst)




if __name__ == "__main__":
    nnUNet_results_dir = '/home/fakai/Docker/tests/val_select_5/nnUNet_results'
    pdcad_output_dir = '/home/fakai/Docker/tests/val_select_5/outputs'
    copy_preds_to_outputs('NM', nnUNet_results_dir + '/Dataset504_PDSegNM/nnUNetTrainer__nnUNetPlans__3d_fullres/fold_0/preds_test_05', pdcad_output_dir)
    copy_preds_to_outputs('QSM', nnUNet_results_dir + '/Dataset505_PDSegQSM/nnUNetTrainer__nnUNetPlans__3d_fullres/fold_0/preds_test_05', pdcad_output_dir)


