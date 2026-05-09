


import os
from core.installation_constants import OUTPUTS_DIR , SELPHY_OUTPUTS_DIR , THERMAL_OUTPUTS_DIR
from datetime import datetime




def save(image , visitor ,output_type):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    visitor_num = str(visitor["visitor_number"]).zfill(3)
    filename = f"{timestamp}_v{visitor_num}_{output_type}.png"

    output_dir = SELPHY_OUTPUTS_DIR if output_type == "selphy" else THERMAL_OUTPUTS_DIR

    filepath = os.path.join(output_dir,filename)
    print(f"SaveManager : Image Saved to {filepath}")

    image.save(filepath)
    return filepath



def get_output_count():
    selphy_count = len(os.listdir(SELPHY_OUTPUTS_DIR))
    thermal_count = len(os.listdir(THERMAL_OUTPUTS_DIR))
    return selphy_count,thermal_count


def clear_outputs():
    for folder in [SELPHY_OUTPUTS_DIR , THERMAL_OUTPUTS_DIR]:
        for file in os.listdir(folder):
            if file.endswith(".png"):
                os.remove(os.path.join(folder,file))
