import cv2
from ultralytics import YOLO
from deep_sort_realtime.deepsort_tracker import DeepSort
import time

# Load YOLOv8 model
model = YOLO('yolov8s.pt')

# Initialize DeepSORT tracker
tracker = DeepSort(max_age=30)

# Video source
cap = cv2.VideoCapture('traffic.mp4')  # Change to 0 for webcam

# Entry & exit line Y positions
line_position1 = 200
line_position2 = 400

# Conversion: distance between lines in meters
real_distance_meters = 5

# Dictionaries for entry times and counted vehicles
entry_times = {}
exit_times = {}
counted_ids = set()
vehicle_count = 0

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.resize(frame, (1024, 768))
    results = model(frame)

    dets_for_tracker = []
    for r in results:
        for box in r.boxes:
            x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()
            conf = box.conf[0].cpu().numpy()
            cls = int(box.cls[0].cpu().numpy())
            if conf > 0.5 and cls == 2:  # Class 2: car
                dets_for_tracker.append(([x1, y1, x2 - x1, y2 - y1], conf, 'car'))

    tracks = tracker.update_tracks(dets_for_tracker, frame=frame)

    # Draw counting lines
    cv2.line(frame, (0, line_position1), (1024, line_position1), (0, 255, 0), 2)
    cv2.line(frame, (0, line_position2), (1024, line_position2), (0, 0, 255), 2)

    for track in tracks:
        if not track.is_confirmed():
            continue

        track_id = track.track_id
        l, t, w, h = track.to_ltrb()
        cx = int((l + w) / 2)
        cy = int((t + h) / 2)

        # Record entry time when crossing entry line
        if track_id not in entry_times and cy < line_position1:
            entry_times[track_id] = time.time()

        # Record exit time when crossing exit line
        if track_id in entry_times and cy > line_position2:
            if track_id not in exit_times:
                exit_times[track_id] = time.time()

                elapsed_time = exit_times[track_id] - entry_times[track_id]
                if elapsed_time > 0:
                    speed = (real_distance_meters / elapsed_time) * 3.6  # km/h
                else:
                    speed = 0

                # Count vehicle only once
                if track_id not in counted_ids:
                    vehicle_count += 1
                    counted_ids.add(track_id)

                # Draw bbox, ID, and speed
                cv2.rectangle(frame, (int(l), int(t)), (int(w), int(h)), (255, 0, 0), 2)
                cv2.putText(
                    frame,
                    f"ID:{track_id} Speed:{int(speed)} km/h",
                    (int(l), int(t) - 10),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.6,
                    (0, 255, 255),
                    2,
                )

        else:
            # Draw bbox and ID only if speed not calculated yet
            cv2.rectangle(frame, (int(l), int(t)), (int(w), int(h)), (255, 0, 0), 2)
            cv2.putText(
                frame,
                f"ID:{track_id}",
                (int(l), int(t) - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (0, 255, 255),
                2,
            )

    # Show total count at top
    cv2.putText(
        frame,
        f"Vehicles Passed: {vehicle_count}",
        (20, 50),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0, 0, 255),
        3,
    )

    cv2.imshow("YOLOv8 Vehicle Count & Speed", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()