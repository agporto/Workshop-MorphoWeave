"""MorphoWeave molar tutorial - folder setup.

Paste into the Slicer Python console (View > Python Console).
Copies 110 molars into train/ and holds 5 out in test/.
"""
import glob, os, shutil

# 1) EDIT THIS: the folder you extracted from data.zip
DATA = os.path.expanduser("~/Downloads/data/molar/2026_06-12_19_24_15")

# 2) Where the tutorial will work (created for you)
WORK = os.path.expanduser("~/molar_tutorial")

HELD_OUT = ["a10", "h08", "k01", "q02", "x02"]   # 5 molars kept out of the atlas

if not os.path.isdir(os.path.join(DATA, "alignedModels")):
    raise SystemExit(f"Can't find alignedModels/ inside {DATA} - check the DATA path above.")

for sub in ("train/models", "train/landmarks", "test/models", "test/landmarks",
            "test/predicted", "output", "segmentation"):
    os.makedirs(os.path.join(WORK, sub), exist_ok=True)

for mesh in glob.glob(os.path.join(DATA, "alignedModels", "*.ply")):
    stem = os.path.basename(mesh)[:-len(".ply")]
    lms = os.path.join(DATA, "alignedLMs", stem + ".mrk.json")
    split = "test" if stem.split("_")[0] in HELD_OUT else "train"
    shutil.copy(mesh, os.path.join(WORK, split, "models"))
    shutil.copy(lms, os.path.join(WORK, split, "landmarks"))

for split in ("train", "test"):
    print(split, len(os.listdir(os.path.join(WORK, split, "models"))), "molars")
