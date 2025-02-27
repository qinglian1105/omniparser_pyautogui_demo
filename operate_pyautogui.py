from omni.omni_scanner import process_image
from PIL import Image
import os
import time
import base64
import io
import pyautogui
import json


INPUT_PATH = "input"
OUTPUT_PATH = "output"
IMG_NAME = "screen_dock.png"
ICON_FILE = "icon_info.json"
IMG_PARAMS = {
    "box_threshold": 0.05,
    "iou_threshold": 0.1,
    "use_paddleocr": True,
    "imgsz": 640,
}
CONTENTS = {"content_iterm": "related to currency", 
            "content_cmd_line": "number 1"}


def prepare_png(t):
    show_dock = {"x": 856, "y": 1151}
    pyautogui.moveTo(**show_dock, duration=1)
    time.sleep(1)
    screen_dock = pyautogui.screenshot()
    screen_dock.save(os.path.join(INPUT_PATH, IMG_NAME))
    print(f"PID: {os.getpid()} ({t})")  
    print(f"---> '{IMG_NAME}' alread saved...")


def save_parsed_img(img_b64, file_name):
    image = Image.open(io.BytesIO(base64.b64decode(img_b64)))
    save_file = f"detected_{file_name}"
    image.save(os.path.join(OUTPUT_PATH, save_file))
    print(f"---> '{save_file}' alread saved...")


def save_paresed_json(ds):
    icon_file = os.path.join(OUTPUT_PATH, ICON_FILE)
    with open(icon_file, "w") as fp:
        json.dump(ds, fp)
    print(f"---> '{ICON_FILE}' alread saved...")


def get_icon_bbox(ds, contents):
    icons = ds["icon_content"]    
    i = 0
    bboxs = dict()
    for k, v in contents.items():
        for icon in icons:
            icon_str = icon["content"]
            if v in icon_str:
                bboxs[k] = icon["bbox"]
                i = i + 1
            if i == 2:
                break    
    return bboxs


def bbox_to_coords(bbox, screen_width, screen_height):
    xmin, ymin, xmax, ymax = bbox
    x_center = int((xmin + xmax) / 2 * screen_width)
    y_center = int((ymin + ymax) / 2 * screen_height)
    return x_center, y_center


def click_icon(bbox):
    screen_width, screen_height = pyautogui.size()
    x, y = bbox_to_coords(bbox, screen_width, screen_height)
    pyautogui.moveTo(x, y, duration=0.5)
    time.sleep(3)
    pyautogui.click()
    print(f"---> Click on: x={x}, y={y}")


def write_to_icon(bbox):
    screen_width, screen_height = pyautogui.size()
    x, y = bbox_to_coords(bbox, screen_width, screen_height)
    pyautogui.moveTo(x, y, duration=0.2)
    print(f"---> Move to: x={x}, y={y}")
    time.sleep(1) 
    pyautogui.click()       
    write_words = 'sh omni_parser.sh'
    pyautogui.write(write_words)
    pyautogui.press("enter")
    print(f"---> Run CMD: {write_words}  ({pyautogui.position()})")


def main():    
    t = time.strftime('%Y-%m-%d %H:%M:%S')     
    time.sleep(3) 
    prepare_png(t)

    screen_width, screen_height = pyautogui.size()
    print(f"The size of current screen: {screen_width} x {screen_height}")
    
    img_input = Image.open(os.path.join(INPUT_PATH, IMG_NAME))
    ds = process_image(img_input, IMG_PARAMS)
    if ds["is_success"]: 
        save_paresed_json(ds["icon_content"])   
        save_parsed_img(ds["img_b64"], IMG_NAME)       
        bboxs = get_icon_bbox(ds, CONTENTS)

        show_dock = {"x": 856, "y": 1151}
        pyautogui.moveTo(**show_dock, duration=1)
        time.sleep(1)

        click_icon(bboxs["content_iterm"])
        write_to_icon(bboxs["content_cmd_line"])

        t = time.strftime('%Y-%m-%d %H:%M:%S')
        print(f"Finish: {os.path.basename(__file__)} ({t})")    
        print("-"*30)
    else:
        print("-"*30)
        print(ds["error"])
        print("-"*30)


if __name__ == "__main__":
    main()