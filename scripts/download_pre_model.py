import os
import shutil
import torch
import requests
import gdown


def download_file(url, output_path, chunk_size=8192):
    """
    下載檔案並支援 large file（streaming）
    """
    response = requests.get(url, stream=True, timeout=60)
    response.raise_for_status()

    with open(output_path, "wb") as f:
        for chunk in response.iter_content(chunk_size=chunk_size):
            if chunk:
                f.write(chunk)


def process_pretrained_model(url, target_dir, final_name, tar=False, is_gdrive=True):
    """
    下載預訓練模型，選擇是否包成 .tar
    """
    os.makedirs(target_dir, exist_ok=True)
    final_path = os.path.join(target_dir, final_name)

    if os.path.exists(final_path):
        print(f"📁 模型已存在，跳過下載: {final_name}")
        return

    tmp_name = final_name + ".tmp"
    tmp_path = os.path.join(target_dir, tmp_name)

    print(f"⬇️ Downloading pretrained model: {final_name}")

    try:
        if not is_gdrive:
            download_file(url, tmp_path)
        else:
            gdown.download(url, tmp_path, quiet=False, fuzzy=True)

        if os.path.getsize(tmp_path) < 1024 * 1024:
            raise ValueError("File too small, 可能下載失敗")

        # 如果要包成 .tar
        if tar:
            state_dict = torch.load(tmp_path, map_location='cpu')
            checkpoint = {'state_dict': state_dict}
            torch.save(checkpoint, final_path)
            os.remove(tmp_path)
            print(f"✅ Completed and packaged as .tar: {final_name}\n")
        else:
            shutil.move(tmp_path, final_path)
            print(f"✅ Completed: {final_name}\n")

    except Exception as e:
        print(f"❌ Failed to download {final_name}: {e}\n")
        if os.path.exists(tmp_path):
            os.remove(tmp_path)


pretrained_models = [
    {
        "url": "https://drive.google.com/file/d/1XB4v1cOZSRCBnGWEcEP61PeQwSODmcUM/view?usp=drive_link",
        "dir": "pre_models",
        "name": "resnext101_ibn_a.pth.tar",
        "tar": True,
        "is_google_drive": True,
    },
]

for model in pretrained_models:
    process_pretrained_model(
        model["url"],
        model["dir"],
        model["name"],
        tar=model.get("tar", False),
        is_gdrive= model.get("is_google_drive", False)
    )
