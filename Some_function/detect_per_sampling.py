import cv2
from ultralytics import YOLO


# 加載 YOLO 模型
model = YOLO('runs/segment/train5/weights/best.pt') 

# 開啟影片
cap = cv2.VideoCapture('output2.mp4')  # 替換為你的影片路徑

# 設置輸出影片參數
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
output_path = 'output_video_v2.mp4'
fps = cap.get(cv2.CAP_PROP_FPS)
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

frame_count = 0
detections = []  # 儲存偵測的物件
order_status = "Unknown"  # 儲存順序狀態（"Correct" 或 "Wrong"）
detect_count = [0, 1, 5, 7, 13, 15, 17, 23]

y_start_point = int(height * 3 / 11)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break
    
    # 每 30 幀進行幾次偵測（in detect_count）
    if frame_count % 30 in detect_count:
        # 裁剪出畫面的左半部分（寬度的三分之二）
        cropped_frame = frame[y_start_point:, :int(width * 2 / 3)]
        
        # 使用 YOLO 模型偵測物體
        results = model(cropped_frame, conf=0.67)
        
        # 清空舊的偵測結果
        detections = []
        
        # 獲取新的邊界框和標籤，並按照 x 座標排序
        for result in results:
            for box in result.boxes:
                x1, y1, x2, y2 = map(int, box.xyxy[0])  # 邊界框座標
                confidence = box.conf[0]  # 置信度
                label = result.names[int(box.cls[0])]  # 類別名稱
                detections.append((x1, y1, x2, y2, label, confidence))
        
        # 按 x 座標排序
        detections.sort(key=lambda x: x[0])
        
        # 檢查排序是否正確
        detect_status = generate_code(detections, names_to_code)
        if detect_status == 'DIIBG':
            order_status = "Correct"
        else:
            order_status = "Wrong"
    
    # 在畫面上顯示上一次偵測的結果
    label_y = 20  # 初始 Y 座標
    for (x1, y1, x2, y2, label, confidence) in detections:
        # 繪製邊界框
        cv2.rectangle(frame, (x1, y1+y_start_point), (x2, y2+y_start_point), (0, 255, 0), 2)
        
        # 在左上方顯示標籤資訊
        label_text = f'{label} {confidence:.2f}'
        cv2.putText(frame, label_text, (10, label_y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
        label_y += 20  # 每個標籤向下移動 20 像素

    # 根據序列狀態顯示顏色
    if order_status == "Correct":
        status_color = (255, 0, 0)  # 藍色
    else:
        status_color = (0, 0, 255)  # 紅色
        
    # 顯示排序狀態（Correct 或 Wrong）
    cv2.putText(frame, f'Sequence Status: {order_status}', (int(width//2+30), int(height*2//11)), cv2.FONT_HERSHEY_SIMPLEX, 0.6, status_color, 2)

    # 將結果寫入輸出影片
    out.write(frame)

    cv2.imshow('YOLO Detection', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    # 增加幀計數器
    frame_count += 1

# 釋放資源
cap.release()
out.release()
cv2.destroyAllWindows()
