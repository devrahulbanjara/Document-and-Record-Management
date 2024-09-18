import cv2

def perform_ocr(highest_conf_boxes,ocr,predicted_class_label,collected_texts,img_array, img_bgr):
    for label, (box, confidence) in highest_conf_boxes.items():
        x1, y1, x2, y2 = box
        
        height, width = img_bgr.shape[:2]
        
        x1 = max(0, x1)
        y1 = max(0, y1)
        x2 = min(width, x2)
        y2 = min(height, y2)

        cropped_img = img_array[y1:y2, x1:x2]

        if predicted_class_label == "Citizenship":
            ocr_result = ocr.readtext(cropped_img)

            for detection in ocr_result:
                text = detection[1]
                collected_texts[label].append(text)
        else:
            ocr_result = ocr.ocr(cropped_img, cls=True)
            text_detected = " ".join([word_info[1][0] for word_info in ocr_result[0] if word_info[1]])
            collected_texts[label].append(text_detected.strip()) 

        color = (255, 0, 0)
        font_scale = 1.2
        font_thickness = 2

        cv2.rectangle(img_bgr, (x1, y1), (x2, y2), color, 2)
        cv2.putText(img_bgr, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, font_scale, color, font_thickness)
    
    return