import sys
import os
import numpy as np

sys.path.append('.')
from lib.data.datasets.veri import VeRi

def generate_veri_txt(distmat_path, output_dir, dataset_root):
    # 1. 載入 VeRi 資料集
    dataset = VeRi(root=dataset_root)
    
    # 2. 載入距離矩陣
    print(f"Loading distmat from {distmat_path}...")
    if not os.path.exists(distmat_path):
        print(f"Error: {distmat_path} 不存在，請檢查 test.sh 是否有設定 TEST.WRITE_RESULT True")
        return
    distmat = np.load(distmat_path)
    
    num_q, num_g = distmat.shape
    print(f"Distmat shape: {num_q} queries x {num_g} gallery images")

    # 3. 排序
    print("Sorting indices...")
    indices = np.argsort(distmat, axis=1)
    
    # 4. 建立 Gallery 索引到檔名的映射
    gallery_names = [os.path.basename(p) for p, _, _ in dataset.gallery]
    
    # 5. 寫入結果檔
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    output_txt_path = os.path.join(output_dir, 'track2.txt')
    print(f"Writing results to {output_txt_path}...")
    
    with open(output_txt_path, 'w') as f:
        for i in range(num_q):
            # 取出前 100 名的索引
            top_indices = indices[i, :100]
            top_names = [gallery_names[idx] for idx in top_indices]
            f.write(' '.join(top_names) + '\n')
            
    print("Done!")

if __name__ == '__main__':
    DISTMAT_PATH = './output/veri/size320/distmat.npy'
    OUTPUT_DIR = './output/veri/submit/'
    DATASET_ROOT = './datasets'
    
    generate_veri_txt(DISTMAT_PATH, OUTPUT_DIR, DATASET_ROOT)