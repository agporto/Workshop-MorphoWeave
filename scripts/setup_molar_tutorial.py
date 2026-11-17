"""MorphoWeave molar tutorial - folder setup.

Paste into the Slicer Python console (View > Python Console).
Copies 110 molars into train/ and holds 5 out in test/.
Works on Windows, macOS and Linux.
"""
import glob, os, shutil

# 1) EDIT THIS: where you extracted data.zip. Paste the path between the quotes as-is;
#    the r"..." keeps Windows backslashes working. Examples:
#      Windows: r"C:\Users\you\Downloads\data"
#      macOS:   r"~/Downloads/data"
#      Linux:   r"~/Downloads"
DATA = r"~/Downloads/data"

# 2) Where the tutorial will work (created for you)
WORK = os.path.expanduser("~/molar_tutorial")

HELD_OUT = ["a10", "h08", "k01", "q02", "x02"]   # 5 molars kept out of the atlas

# Find molar/<run>/alignedModels under DATA, wherever your unzip tool put it
DATA = os.path.expanduser(DATA.strip().strip('"'))
found = [d for d in sorted(glob.glob(os.path.join(DATA, "**", "alignedModels"), recursive=True))
         if "molar" in os.path.normpath(d).split(os.sep)]

if not found:
    raise FileNotFoundError(f"No molar/.../alignedModels folder found under {DATA}. Check the DATA path above.")

SRC = os.path.dirname(found[0])
print("Using data in", SRC)
for sub in ("train/models", "train/landmarks", "test/models", "test/landmarks",
            "test/predicted", "output", "segmentation"):
    os.makedirs(os.path.join(WORK, sub), exist_ok=True)

for mesh in glob.glob(os.path.join(SRC, "alignedModels", "*.ply")):
    stem = os.path.basename(mesh)[:-len(".ply")]
    lms = os.path.join(SRC, "alignedLMs", stem + ".mrk.json")
    split = "test" if stem.split("_")[0] in HELD_OUT else "train"
    shutil.copy(mesh, os.path.join(WORK, split, "models"))
    shutil.copy(lms, os.path.join(WORK, split, "landmarks"))

for split in ("train", "test"):
    print(split, len(os.listdir(os.path.join(WORK, split, "models"))), "molars ->", os.path.join(WORK, split))
