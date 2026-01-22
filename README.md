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

由於 PyTorch 需依照系統架構（x86 / ARM）與 CUDA 環境選擇對應版本，請依官方指引自行安裝，但由於要使用 apex 套件，不要安裝太新的版本 (本次使用 1.13.1)：

👉 [https://pytorch.org/get-started/locally/](https://pytorch.org/get-started/locally/)

```bash
conda install pytorch==1.13.1 torchvision==0.14.1 torchaudio==0.13.1 pytorch-cuda=11.6 -c pytorch -c nvidia
```

[apex](https://github.com/NVIDIA/apex)安裝 (非常難搞，整個步驟最難的部分...):

```bash
git clone https://github.com/NVIDIA/apex
cd apex
git checkout 22.04-dev
```

打開 setup.py，禁用 ninja。

```bash
cmdclass={"build_ext": BuildExtension} if ext_modules else {} # 原本
cmdclass={"build_ext": BuildExtension.with_options(use_ninja=False)} if ext_modules else {}, # 修改後
```

開始編譯~

```bash
# Using pip config-settings (pip >= 23.1)
pip install -v --disable-pip-version-check --no-cache-dir --no-build-isolation --config-settings "--build-option=--cpp_ext" --config-settings "--build-option=--cuda_ext" ./

# For older pip versions
pip install -v --disable-pip-version-check --no-cache-dir --no-build-isolation --global-option="--cpp_ext" --global-option="--cuda_ext" ./
```

可能會遇到的問題: [fatal error: cusolverDn.h: No such file or directory](https://github.com/deepspeedai/DeepSpeed/issues/2684)


### 資料集下載

```bash
python scripts/prepare_datasets.py
python scripts/download_pre_model.py
```

## step 1 Prepare Data

弱監督檢測增強。訓練了一個初始的車輛 ReID 模型，以獲取每張圖像的熱圖響應，並設定一個閾值來獲取大於該閾值的邊界框。與監督檢測方法相比，它能更緊密地裁剪車輛，專注於 Re-ID 模型的注意力區域。在弱監督檢測之後，獲得了訓練集和測試集的裁剪副本。訓練集與原始圖像一同使用，使數據集翻了一倍。

```bash
# 訓練初始車輛 ReID 模型
scripts/augmix.sh

# 裁切 datasets/AIC20_ReID 的訓練資料並放置到 datasets/AIC20_ReID_Cropped
scripts/weakly_supervised_crop_aug.sh
```