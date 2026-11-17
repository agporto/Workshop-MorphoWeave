"""MorphoWeave molar tutorial - compare predicted and manual landmarks.

Paste into the Slicer Python console after the Batch run.
Errors are reported as a percentage of each tooth's bounding-box diagonal.
"""
import glob, json, os
import numpy as np
import vtk

# EDIT THIS: the molar_tutorial folder inside the workshop files (Windows backslashes are fine)
WORK = os.path.expanduser(r"~/Downloads/Workshop-MorphoWeave-main/molar_tutorial")

if not os.path.isdir(os.path.join(WORK, "test", "predicted")):
    raise FileNotFoundError(f"{WORK} doesn't look like the molar_tutorial folder. Check the WORK path above.")

def read_points(path):
    with open(path, encoding="utf-8") as f:
        markup = json.load(f)["markups"][0]
    pts = np.array([p["position"] for p in markup["controlPoints"]])
    return pts * [-1, -1, 1] if markup.get("coordinateSystem", "LPS") == "LPS" else pts

def tooth_size(mesh_path):
    reader = vtk.vtkPLYReader(); reader.SetFileName(mesh_path); reader.Update()
    b = reader.GetOutput().GetBounds()
    return np.linalg.norm([b[1] - b[0], b[3] - b[2], b[5] - b[4]])

print(f"{'specimen':<16}{'mean error':>12}{'worst point':>14}")
for pred_path in sorted(glob.glob(os.path.join(WORK, "test", "predicted", "*.mrk.json"))):
    name = os.path.basename(pred_path).replace(".mrk.json", "")
    manual = read_points(os.path.join(WORK, "test", "landmarks", name + ".mrk.json"))
    errors = np.linalg.norm(read_points(pred_path) - manual, axis=1)
    errors = 100 * errors / tooth_size(os.path.join(WORK, "test", "models", name + ".ply"))
    print(f"{name:<16}{errors.mean():>11.1f}%{errors.max():>13.1f}%  (point {errors.argmax() + 1})")
