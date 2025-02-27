import io
import torch
import os
from PIL import Image
from omni.util.utils import check_ocr_box, get_yolo_model, get_caption_model_processor, get_som_labeled_img


YOLO_MODEL = get_yolo_model(model_path='omni/weights/icon_detect/model.pt')
CAPTION_MODEL_PROCESSOR = get_caption_model_processor(
    model_name="florence2", 
    model_name_or_path="omni/weights/icon_caption_florence"
)  
DEVICE = torch.device('cuda' if torch.cuda.is_available() else 'cpu')


def process_image(img_input, img_params):
    try:                                          
        image_save_path = 'omni/imgs/img_tmp.png'
        img_input.save(image_save_path)
        image = Image.open(image_save_path)
                      
        box_overlay_ratio = image.size[0] / 3200
        draw_bbox_config = {
            'text_scale': 0.8 * box_overlay_ratio,
            'text_thickness': max(int(2 * box_overlay_ratio), 1),
            'text_padding': max(int(3 * box_overlay_ratio), 1),
            'thickness': max(int(3 * box_overlay_ratio), 1),
        }

        ocr_bbox_rslt, is_goal_filtered = check_ocr_box(
            image_save_path,
            display_img=False,
            output_bb_format='xyxy',
            goal_filtering=None,
            easyocr_args={'paragraph': False, 'text_threshold': 0.9},        
            use_paddleocr=img_params["use_paddleocr"]
        )
        text, ocr_bbox = ocr_bbox_rslt        

        dino_labled_img, label_coordinates, parsed_content_list = get_som_labeled_img(
            image_save_path,
            YOLO_MODEL,        
            BOX_TRESHOLD=img_params["box_threshold"],
            output_coord_in_ratio=True,
            ocr_bbox=ocr_bbox,
            draw_bbox_config=draw_bbox_config,
            caption_model_processor=CAPTION_MODEL_PROCESSOR,
            ocr_text=text,        
            iou_threshold=img_params["iou_threshold"],
            imgsz=img_params["imgsz"],
        )
        
        icons = []
        for idx, cnt in enumerate(parsed_content_list):
            cnt['icon'] = idx
            icons.append(cnt)                     
        
        res = {"is_success": True,
               "img_b64": dino_labled_img,  
               "icon_content": icons, 
               "label_coordinates": label_coordinates
               } 
        
        os.remove(image_save_path)   

        return res
    
    except Exception as e:        
        return {"is_success": False, "error": str(e)}
        
    
    