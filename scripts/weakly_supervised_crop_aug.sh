set -e
# 設定 Trap：如果腳本中途失敗或結束，都會嘗試還原 aicity20.py
trap 'echo "🚨 發生錯誤或腳本結束，正在還原 aicity20.py..."; mv lib/data/datasets/aicity20.py.bak lib/data/datasets/aicity20.py 2>/dev/null || true; echo "✅ 還原完成"' EXIT

# 1️⃣ 備份 aicity20.py
cp lib/data/datasets/aicity20.py lib/data/datasets/aicity20.py.bak

# 2️⃣ 修改 aicity20.py
# 2.1: 註解第 49 行 (避免載入還不存在的 aug 資料)
sed -i '49s/^/#/' lib/data/datasets/aicity20.py
# 2.2: 暫時將 dataset_aug_dir 修改為 'AIC20_ReID' (騙過 Loader 去讀原始圖)
sed -i "s/dataset_aug_dir = 'AIC20_ReID_Cropped'/dataset_aug_dir = 'AIC20_ReID'/" lib/data/datasets/aicity20.py

echo "✅ 修改 aicity20.py 完成 (Line 49 註解 & 指向原始資料夾)"

python tools/aicity20/weakly_supervised_crop_aug.py --config_file='configs/aicity20.yml' \
MODEL.DEVICE_ID "('0')" \
MODEL.NAME "('resnet50_ibn_a')" \
MODEL.MODEL_TYPE "baseline" \
DATASETS.TRAIN "('aicity20',)" \
DATASETS.TEST "('aicity20',)" \
DATALOADER.SAMPLER 'softmax' \
DATASETS.ROOT_DIR "('./datasets')" \
MODEL.PRETRAIN_CHOICE "('self')" \
TEST.WEIGHT "('./output/aicity20/augmix/best.pth')"

# 4️⃣ 還原 aicity20.py
# 因為後續訓練需要它指向正確的 AIC20_ReID_Cropped
mv lib/data/datasets/aicity20.py.bak lib/data/datasets/aicity20.py
echo "✅ aicity20.py 已還原為原始狀態"
trap - EXIT

# 5️⃣ 移動生成的裁切資料
SOURCE_DIR="./output/aicity20/augmix"
DEST_DIR="./datasets/AIC20_ReID_Cropped"

echo "📦 開始移動資料..."
echo "   來源: $SOURCE_DIR"
echo "   目的: $DEST_DIR"

# 確保目的資料夾存在
if [ ! -d "$DEST_DIR" ]; then
    echo "   📁 創建資料夾: $DEST_DIR"
    mkdir -p "$DEST_DIR"
fi

# 移動 image_train, image_query, image_test
# 使用 -f 強制覆蓋，避免如果有舊資料卡住
if [ -d "$SOURCE_DIR/image_train" ]; then
    mv -f "$SOURCE_DIR/image_train" "$DEST_DIR/"
    echo "   ✅ image_train 移動完成"
else
    echo "   ⚠️ 警告: 找不到 $SOURCE_DIR/image_train"
fi

if [ -d "$SOURCE_DIR/image_query" ]; then
    mv -f "$SOURCE_DIR/image_query" "$DEST_DIR/"
    echo "   ✅ image_query 移動完成"
else
    echo "   ⚠️ 警告: 找不到 $SOURCE_DIR/image_query"
fi

if [ -d "$SOURCE_DIR/image_test" ]; then
    mv -f "$SOURCE_DIR/image_test" "$DEST_DIR/"
    echo "   ✅ image_test 移動完成"
else
    echo "   ⚠️ 警告: 找不到 $SOURCE_DIR/image_test"
fi

echo "🎉 所有步驟完成！"