import os
import os.path as osp
import xml.etree.ElementTree as ET
import random

# 設定路徑
DATA_ROOT = './datasets/AIC20_ReID'
LABEL_PATH = osp.join(DATA_ROOT, 'train_label.xml')
OUTPUT_DIR = osp.join(DATA_ROOT, 'trainval_partial')

def generate_split():
    if not osp.exists(LABEL_PATH):
        print(f"錯誤: 找不到標籤檔案 {LABEL_PATH}")
        return

    if not osp.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
        print(f"建立資料夾: {OUTPUT_DIR}")

    # 解析 XML
    with open(LABEL_PATH, 'r', encoding='gbk', errors='ignore') as f:
        xml_content = f.read()
    root = ET.fromstring(xml_content)
    items = root.find('Items')

    # 整理資料: {pid: [info_dict, ...]}
    data_by_pid = {}
    
    # 讀取所有圖片資訊
    # 格式需求: pid_camid_trackid_imagename
    # XML 屬性: vehicleID, cameraID, imageName
    # 注意: XML 裡沒有 trackID，我們需要為了格式相容偽造一個，或者從檔名推測(如果有的話)。
    # 觀察 aicity20_ReCam.py 的讀取方式: pid, camid, trackid, image_name = line.split('_')
    # 所以我們必須生成這種格式的字串。
    
    print("正在解析 train_label.xml ...")
    for obj in items:
        pid = int(obj.attrib['vehicleID'])
        camid = obj.attrib['cameraID'] # 格式如 c002
        img_name = obj.attrib['imageName']
        
        if pid not in data_by_pid:
            data_by_pid[pid] = []
            
        # 這裡我們暫時將 trackid 設為 t000，因為 ReCam 任務主要看 CamID，TrackID 不影響讀取
        # 格式範例: 0001_c002_t000_000123.jpg
        formatted_line = f"{pid:04d}_{camid}_t000_{img_name}"
        data_by_pid[pid].append(formatted_line)

    # 取得所有 PID 並排序
    all_pids = sorted(data_by_pid.keys())
    print(f"總共發現 {len(all_pids)} 個車輛 ID")

    # 根據作者邏輯分割
    # "1-95为测试集, 241-478为训练集" (注意: 這裡的數字可能是指排序後的順序，或是真實ID)
    # 為了保險起見，我們依照排序後的順序切分
    # 前 95 個 ID 作為驗證集 (Test/Query)
    # 剩下的 ID 作為訓練集 (Train)
    
    val_pids = all_pids[:95]
    train_pids = all_pids[95:]
    
    print(f"分配 {len(val_pids)} 個 ID 給驗證集 (Test/Query)")
    print(f"分配 {len(train_pids)} 個 ID 給訓練集 (Train)")

    # 生成檔案內容
    train_lines = []
    test_lines = []
    query_lines = []

    # 1. 構建訓練集 (train.txt)
    for pid in train_pids:
        train_lines.extend(data_by_pid[pid])

    # 2. 構建驗證集 (test.txt) 和 查詢集 (query.txt)
    # 作者註釋: "测试集中随机取500张作为query"
    
    val_images = []
    for pid in val_pids:
        val_images.extend(data_by_pid[pid])
    
    # 全部放入 test.txt (Gallery)
    test_lines = val_images[:]
    
    # 隨機選 500 張放入 query.txt
    random.seed(42)
    if len(val_images) > 500:
        query_lines = random.sample(val_images, 500)
    else:
        query_lines = val_images # 如果不夠就全放

    # 寫入檔案
    def write_txt(filename, lines):
        path = osp.join(OUTPUT_DIR, filename)
        with open(path, 'w') as f:
            for line in lines:
                f.write(line + '\n')
        print(f"已生成 {filename}: {len(lines)} 行")

    write_txt('train.txt', train_lines)
    write_txt('test.txt', test_lines)
    write_txt('query.txt', query_lines)
    
    # 生成一個空的 track 檔以免報錯 (雖然 ReCam 可能用不到)
    write_txt('test_track.txt', []) 

if __name__ == '__main__':
    generate_split()