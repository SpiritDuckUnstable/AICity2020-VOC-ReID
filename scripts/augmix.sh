set -e
trap 'echo "🚨 發生錯誤，還原 aicity20.py"; mv lib/data/datasets/aicity20.py.bak lib/data/datasets/aicity20.py' EXIT

# 1️⃣ 備份 aicity20.py
cp lib/data/datasets/aicity20.py lib/data/datasets/aicity20.py.bak

# 2️⃣ 註解第 49 行
sed -i '49s/^/#/' lib/data/datasets/aicity20.py
echo "✅ 註解 aicity20.py 第 49 行完成"

python tools/train.py --config_file='configs/aicity20.yml' \
MODEL.DEVICE_ID "('0')" \
MODEL.MODEL_TYPE "baseline" \
MODEL.NAME "('resnet50_ibn_a')" \
MODEL.PRETRAIN_PATH "('./pre_models/resnet50_ibn_a.pth.tar')" \
SOLVER.LR_SCHEDULER 'cosine_step' \
DATALOADER.NUM_INSTANCE 16 \
MODEL.ID_LOSS_TYPE 'circle' \
SOLVER.WARMUP_ITERS 0 \
SOLVER.MAX_EPOCHS 12 \
SOLVER.COSINE_MARGIN 0.35 \
SOLVER.COSINE_SCALE 64 \
SOLVER.FREEZE_BASE_EPOCHS 2 \
MODEL.TRIPLET_LOSS_WEIGHT 1.0 \
DATASETS.TRAIN "('aicity20',)" \
DATASETS.TEST "('veri',)" \
DATASETS.ROOT_DIR "('./datasets')" \
OUTPUT_DIR "('./output/aicity20/augmix/')"

mv lib/data/datasets/aicity20.py.bak lib/data/datasets/aicity20.py
echo "✅ 還原 aicity20.py 完成"

trap - EXIT