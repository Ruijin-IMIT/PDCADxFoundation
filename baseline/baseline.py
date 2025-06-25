import os
import shutil
import subprocess


import shlex
import os
import signal
import sys
import time
import threading
from subprocess import Popen, PIPE

from RRMediCa.data_process import annotation_gen, image_crop
from RRMediCa import test

def run_command(command):
    process = Popen(shlex.split(command), stdout=PIPE)
    st = time.time()
    while True:
        output = process.stdout.readline().rstrip().decode('utf-8')
        if output == '' and process.poll() is not None:
            break
        if output:
            print(output.strip())
        # if time.time() - st > 5:
        #     os.kill(process.pid, signal.SIGTERM) # SIGSTOP SIGQUIT SIGKILL SIGABRT
        #     break
    rc = process.poll()
    return rc

input_dir = ''
output_dir = ''


def nnunet_inference(nm_dir_pairs, qsm_dir_pairs):
    '''
    customized nnunet inference function. Make sure the folders and images have been prepared.
    Change the os.environ['nnUNet_results'], Task No., Fold No. accordingly
    nm_dir_pairs: list of tuples (input_dir, output_dir)
    qsm_dir_pairs: list of tuples (input_dir, output_dir)
    '''
    NM_Task = 504
    QSM_Task = 505

    for in_dir, out_dir in nm_dir_pairs:
        NM_nnunet_predict_cmd = f"nnUNetv2_predict -d {NM_Task} -i {in_dir} -o {out_dir} -c 3d_fullres -f 0"
        t = threading.Thread(target=run_command, args=(NM_nnunet_predict_cmd,))
        t.start()
        t.join()

    for in_dir, out_dir in qsm_dir_pairs:
        NM_nnunet_predict_cmd = f"nnUNetv2_predict -d {QSM_Task} -i {in_dir} -o {out_dir} -c 3d_fullres -f 0"
        t = threading.Thread(target=run_command, args=(NM_nnunet_predict_cmd,))
        t.start()
        t.join()

def prepare_nnunet_dir(output_dir):
    nnunet_dir = os.path.join(output_dir, 'nnunet')
    os.makedirs(nnunet_dir, exist_ok=True)
    NM_nnunet_in = os.path.join(nnunet_dir, 'NM_nnunet_in')
    os.makedirs(NM_nnunet_in, exist_ok=True)
    NM_nnunet_out = os.path.join(nnunet_dir, 'NM_nnunet_out')
    os.makedirs(NM_nnunet_out, exist_ok=True)
    QSM_nnunet_in = os.path.join(nnunet_dir, 'QSM_nnunet_in')
    os.makedirs(QSM_nnunet_in, exist_ok=True)
    QSM_nnunet_out = os.path.join(nnunet_dir, 'QSM_nnunet_out')
    os.makedirs(QSM_nnunet_out, exist_ok=True)
    return nnunet_dir, NM_nnunet_in, NM_nnunet_out, QSM_nnunet_in, QSM_nnunet_out

def save_result_csv(csv_file, case_names, preds, gts):
    content = ''
    for c, p, t in zip(case_names, preds, gts):
        case_name = '_'.join(c.split('_')[:2])
        pred = int(p[0]) # only one label: the 1st one
        content += f'{case_name},{pred}\n'
    content = content[:-1]
    with open(csv_file, 'w') as f:
        f.write(content)
    print(f"Results saved to {csv_file}")
    return

def main_entry(input_dir, output_dir, temp_dir):
    print(f"input_dir={input_dir}, output_dir={output_dir}, temp_dir={temp_dir}")
    nnunet_dir, NM_nnunet_in, NM_nnunet_out, QSM_nnunet_in, QSM_nnunet_out = prepare_nnunet_dir(temp_dir)
    case_names = os.listdir(input_dir)
    case_names = [c for c in case_names if 'RJPD' in c]

    # Stage 1: do the segmentation, predict the mask for NM.nii.gz and QSM.nii.gz
    # call nnunet, pass the model path, set output dir
    for c in case_names:
        case_dir = os.path.join(input_dir, c)
        nm_file_path = os.path.join(case_dir, 'NM.nii.gz')
        nm_nnunet_file = f"{c}_NM_0000.nii.gz"
        if os.path.exists(nm_file_path):
            shutil.copy(nm_file_path, os.path.join(NM_nnunet_in, nm_nnunet_file))
        else:
            print(nm_file_path, ' not found')
        qsm_file_path = os.path.join(case_dir, 'QSM.nii.gz')
        qsm_nnunet_file = f"{c}_QSM_0000.nii.gz"
        if os.path.exists(qsm_file_path):
            shutil.copy(qsm_file_path, os.path.join(QSM_nnunet_in, qsm_nnunet_file))
        items = os.listdir(case_dir)

        # copy images to output dir
        output_case_dir = os.path.join(output_dir, c)
        if not os.path.exists(output_case_dir):
            os.makedirs(output_case_dir)
        for i in items:
            if not os.path.exists(os.path.join(output_case_dir, i)):
                shutil.copy(os.path.join(case_dir, i), os.path.join(output_case_dir, i))

    nm_dir_pairs = [(NM_nnunet_in, NM_nnunet_out)]
    qsm_dir_pairs = [(QSM_nnunet_in, QSM_nnunet_out)]
    nnunet_inference(nm_dir_pairs, qsm_dir_pairs)

    # may do some post-processing, before copying to the output dir
    items = os.listdir(NM_nnunet_out)
    items = [i for i in items if '.nii.gz' in i]
    for item in items:
        case_name = '_'.join(item.split('_')[:2])
        output_case_dir = os.path.join(output_dir, case_name)
        src = os.path.join(NM_nnunet_out, item)
        dst = os.path.join(output_case_dir, 'NM_mask.nii.gz')
        shutil.copy(src, dst)
    items = os.listdir(QSM_nnunet_out)
    items = [i for i in items if '.nii.gz' in i]
    for item in items:
        case_name = '_'.join(item.split('_')[:2])
        output_case_dir = os.path.join(output_dir, case_name)
        src = os.path.join(QSM_nnunet_out, item)
        dst = os.path.join(output_case_dir, 'QSM_mask.nii.gz')
        shutil.copy(src, dst)


    # Stage 2: PD classification, generate pd_class.csv
    # first crop the ROIs, prepare for RRMediCa
    database = output_dir
    lesion_base = os.path.join(temp_dir, 'ROIs')
    os.makedirs(lesion_base, exist_ok=True)
    pd_map = {} # label = 0 by default
    annotation_gen.create_annotation_from_mask_RJPD(database, pd_map, [9,10,11,12, 13,14], [1,2])
    image_crop.extract_database_lesions(database, lesion_base)

    # call RRMediCa, output to folder
    ckpts_root = os.environ['ckpts_root']
    case_names, preds, gts = test.test_project_RJPD(lesion_base, ckpts_root)
    csv_file = os.path.join(output_dir, 'pred.csv')
    save_result_csv(csv_file, case_names, preds, gts)


if __name__ == '__main__':
    input_dir = sys.argv[1]
    output_dir = sys.argv[2]
    temp_dir = sys.argv[3]
    model_dir = sys.argv[4]
    print(len(sys.argv), sys.argv)
    if len(sys.argv) != 5:
        print('Usage: python baseline.py input_dir output_dir temp_dir model_dir')
        exit()
    os.environ['nnUNet_results'] = os.path.join(model_dir, 'nnunet/nnUNet_results')
    os.environ['ckpts_root'] = os.path.join(model_dir, 'RRMediCa_ckpts')
    main_entry(input_dir, output_dir, temp_dir)
















