import os
import shutil
import zipfile

import gdown


def flatten_directory(target_dir):
    """
    檢查 target_dir 是否只包含一個子資料夾。
    如果是，將該子資料夾內的內容移動到 target_dir，並刪除空殼。
    """
    items = [
        i
        for i in os.listdir(target_dir)
        if not i.startswith("__") and not i.startswith(".")
    ]

    if len(items) == 1:
        subfolder_name = items[0]
        subfolder_path = os.path.join(target_dir, subfolder_name)

        if os.path.isdir(subfolder_path):
            for item in os.listdir(subfolder_path):
                src = os.path.join(subfolder_path, item)
                dst = os.path.join(target_dir, item)
                shutil.move(src, dst)

            os.rmdir(subfolder_path)


def process_dataset(url, target_dir, zip_name):
    os.makedirs(target_dir, exist_ok=True)

    if len(os.listdir(target_dir)) > 0:
        print(f"📁 目錄 '{target_dir}' 已有內容，跳過下載。")
        return

    print(f"⬇️ Processing: {zip_name}")

    output = gdown.download(url, zip_name, quiet=False, fuzzy=True)
    if not output or os.path.getsize(output) < 1024 * 1024:
        print(f"❌ Skipped {zip_name}: File invalid or too small.")
        if output and os.path.exists(output):
            os.remove(output)
        return

    try:
        print(f"📦 Extracting to '{target_dir}' ...")
        with zipfile.ZipFile(output, "r") as zip_ref:
            zip_ref.extractall(target_dir)

        flatten_directory(target_dir)

        os.remove(output)
        print(f"✅ Completed: {zip_name}\n")

    except zipfile.BadZipFile:
        print(f"❌ Error: {zip_name} is corrupted.\n")


download_list = [
    {
        "url": "https://drive.google.com/file/d/1W1vEirmbwY0UYtueU6bP0v0Lcq5ji_CS/view",
        "dir": "datasets/AIC20_ReID_Simulation",
        "zip": "AIC20_ReID_Simulation.zip",
    },
    {
        "url": "https://drive.google.com/file/d/1gXo9v5XxK-IYHD41l3O158QfLXKVsSrd/view",
        "dir": "datasets/AIC20_ReID",
        "zip": "AIC20_ReID.zip",
    },
    {
        "url": "https://drive.google.com/file/d/0B0o1ZxGs_oVZWmtFdXpqTGl3WUU/view",
        "dir": "datasets/VeRi",
        "zip": "VeRi.zip",
    },
]

for item in download_list:
    process_dataset(item["url"], item["dir"], item["zip"])
