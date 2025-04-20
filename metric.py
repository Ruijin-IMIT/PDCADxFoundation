




import numpy as np
import os
import csv
from medpy.metric.binary import dc, hd
import nibabel as nib

def evaluate_segmentation(gt_data, pred_data, label_dict):
    """
    Evaluate segmentation performance for one sample
    :param gt_data: 3D numpy array of ground truth segmentation
    :param pred_data: 3D numpy array of predicted segmentation
    :param label_dict: Dictionary {structure_name: label_value}
    :return: Dictionary containing evaluation metrics for each structure
    """
    results = {}
    
    for structure, label in label_dict.items():
        # Create binary masks
        gt_binary = (gt_data == label).astype(np.uint8)
        pred_binary = (pred_data == label).astype(np.uint8)
        
        # Calculate metrics
        dice = dc(pred_binary, gt_binary)
        
        try:
            hd_score = hd(pred_binary, gt_binary)
        except:
            # Set Hausdorff distance to inf if one mask is empty
            hd_score = float('inf')
        
        # Calculate volume metrics
        # vol_gt = np.sum(gt_binary.astype(np.float))
        # vol_pred = np.sum(pred_binary.astype(np.float))
        # vol_diff = abs(vol_gt - vol_pred)
        # vol_similarity = 1 - vol_diff / max(vol_gt, vol_pred) if max(vol_gt, vol_pred) > 0 else 0
        
        results[structure] = {
            'Dice': dice,
            'Hausdorff': hd_score,
            # 'Volume_Similarity': vol_similarity,
            # 'Volume_GT': vol_gt,
            # 'Volume_Pred': vol_pred
        }
    
    return results

def process_batch(mr_mod, gt_dir, pred_dir, label_dict, csv_path):
    """
    Process a batch of samples and save results to CSV
    :param gt_dir: Directory containing ground truth NIfTI files
    :param pred_dir: Directory containing predicted NIfTI files
    :param label_dict: Dictionary {structure_name: label_value}
    :param csv_path: Path to save CSV results
    """
    # Get list of sample files (assuming matching filenames in both directories)
    # Check by the gt casenames, mr modalities
    casenames = os.listdir(gt_dir)
    casenames = sorted([c for c in casenames if 'RJPD_' in c])
    gt_files = [os.path.join(gt_dir, c, mr_mod + '_mask.nii.gz') for c in casenames]
    pred_files = [os.path.join(pred_dir, c, mr_mod + '_pred.nii.gz') for c in casenames]
    
    # Prepare CSV headers
    structures = sorted(label_dict.keys())
    metrics = ['Dice', 'Hausdorff'] # , 'Volume_Similarity', 'Volume_GT', 'Volume_Pred'
    headers = ['Sample']
    
    # Create column headers for each structure and metric
    for struct in structures:
        for metric in metrics:
            headers.append(f"{struct}_{metric}")
    
    all_results = []
    
    # Process each sample
    for casename, gt_file, pred_file in zip(casenames, gt_files, pred_files):
        
        
        sample_name = casename + '_' + mr_mod
        
        # if gt_file != pred_file:
        #     print(f"Warning: Filename mismatch - GT: {gt_file}, Pred: {pred_file}")
        #     continue

        # Load NIfTI files
        gt_path = os.path.join(gt_dir, gt_file)
        pred_path = os.path.join(pred_dir, pred_file)
        
        try:
            gt_data = nib.load(gt_path).get_fdata()
            pred_data = nib.load(pred_path).get_fdata()
        except Exception as e:
            print(f"Error loading files for sample {sample_name}: {str(e)}")
            continue
        
        # Evaluate segmentation
        sample_results = evaluate_segmentation(gt_data, pred_data, label_dict)
        
        # Prepare CSV row
        row_data = [sample_name]
        
        for struct in structures:
            struct_results = sample_results.get(struct, {})
            for metric in metrics:
                value = struct_results.get(metric, float('nan'))
                # Format numeric values appropriately
                if isinstance(value, float) and not np.isinf(value):
                    row_data.append(f"{value:.4f}")
                else:
                    row_data.append(str(value))
        
        all_results.append(row_data)
        
        print(f"Processed sample: {sample_name}")
    
    # Calculate average metrics across all samples
    if all_results:
        avg_row = ['Average']
        num_samples = len(all_results)
        
        for col_idx in range(1, len(headers)):
            try:
                # Skip non-numeric values when calculating average
                col_values = [float(row[col_idx]) for row in all_results 
                            if not np.isnan(float(row[col_idx])) and not np.isinf(float(row[col_idx]))]
                if col_values:
                    avg_value = sum(col_values) / len(col_values)
                    avg_row.append(f"{avg_value:.4f}")
                else:
                    avg_row.append('nan')
            except:
                avg_row.append('nan')
        
        all_results.append(avg_row)
    
    # Write to CSV
    with open(csv_path, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(headers)
        writer.writerows(all_results)
    
    print(f"\nEvaluation completed. Results saved to: {csv_path}")


if __name__ == "__main__":
    # Define label dictionary (structure_name: label_value)
    QSM_LABEL_DICT = {
        'CN_r':1,         # Caudate Nucleus, r=right, l=left
        'CN_l':2,
        'Put_r':3,        # Putaman
        'Put_l':4,
        'GP_r':5,         # Globus Pallidus
        'GP_l':6,
        'STN_r':9,        # Subthalamic Nucleus
        'STN_l':10,
        'SN_r': 11,        # Substantia Nigra
        'SN_l': 12,        # Substantia Nigra
        'RN_r': 13,        # Red Nucleus
        'RN_l': 14,        # Red Nucleus
        'DN_r': 15,        # Dentate Nucleus
        'DN_l': 16         # Dentate Nucleus
    }
    NM_LABEL_DICT = {
        'SN_r': 1,        # Substantia Nigra
        'SN_l': 2         # Substantia Nigra
    }
    
    # Directory paths (modify these to your actual paths)
    GT_DIR = '/home/fakai/Docker/tests/val_select_5/ground_truth'      # Directory containing ground truth NIfTI files
    PRED_DIR = '/home/fakai/Docker/tests/val_select_5/outputs'      # Directory containing predicted NIfTI files
    NM_CSV_OUTPUT = os.path.join(PRED_DIR, 'batch_seg_eval_results_nm.csv')
    QSM_CSV_OUTPUT = os.path.join(PRED_DIR, 'batch_seg_eval_results_qsm.csv')
    
    # Check if directories exist
    if not os.path.isdir(GT_DIR):
        raise FileNotFoundError(f"Ground truth directory not found: {GT_DIR}")
    if not os.path.isdir(PRED_DIR):
        raise FileNotFoundError(f"Prediction directory not found: {PRED_DIR}")
    
    # Process all samples in the directories
    process_batch('NM', GT_DIR, PRED_DIR, NM_LABEL_DICT, NM_CSV_OUTPUT)
    process_batch('QSM', GT_DIR, PRED_DIR, QSM_LABEL_DICT, QSM_CSV_OUTPUT)







