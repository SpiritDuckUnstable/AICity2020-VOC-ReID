## 事前準備

### conda 環境

```bash
conda create --name voc-reid python=3.11.14
conda activate voc-reid
```

### 套件安裝

```bash
pip install -r requirements.txt
```


由於 PyTorch 需依照系統架構（x86 / ARM）與 CUDA 環境選擇對應版本，請依官方指引自行安裝：

👉 [https://pytorch.org/get-started/locally/](https://pytorch.org/get-started/locally/)

安裝 [apex](https://github.com/NVIDIA/apex) 庫:

```bash
git clone https://github.com/NVIDIA/apex third_party/apex
python3 third_party/apex/setup.py install
```

## step 1 Prepare Data

弱監督檢測增強。訓練了一個初始的車輛 ReID 模型，以獲取每張圖像的熱圖響應，並設定一個閾值來獲取大於該閾值的邊界框。與監督檢測方法相比，它能更緊密地裁剪車輛，專注於 Re-ID 模型的注意力區域。在弱監督檢測之後，獲得了訓練集和測試集的裁剪副本。訓練集與原始圖像一同使用，使數據集翻了一倍。

```bash
# 訓練初始車輛 ReID 模型
scripts/augmix.sh

# 裁切 datasets/AIC20_ReID 的訓練資料並放置到 datasets/AIC20_ReID_Cropped
scripts/weakly_supervised_crop_aug.sh
```