# Vehicle-Counting-Speed-Estimation
Vehicle Counting & Speed Estimation using YOLOv8 + DeepSORT
This project uses Ultralytics YOLOv8 for real-time object detection and DeepSORT for object tracking to count vehicles and estimate their speed as they cross two virtual lines in a video.

🎯 Features
✅ Detects vehicles using YOLOv8
✅ Tracks vehicles uniquely with DeepSORT
✅ Calculates vehicle speed based on time taken to cross two lines
✅ Displays vehicle ID and speed on bounding boxes
✅ Shows total vehicle count on screen
✅ Uses OpenCV for video processing and display

📂 Project Structure
Copy
Edit
├── vehicle_count_speed_yolov8.py
├── traffic.mp4
├── README.md
⚡ Requirements
Install dependencies:

bash
Copy
Edit
pip install ultralytics deep_sort_realtime opencv-python
▶️ How to Run
Place your input video as traffic.mp4 in the project folder (or change the filename in the code).

Run:

bash
Copy
Edit
python vehicle_count_speed_yolov8.py
Press 'q' to quit the video window.

⚙️ How it Works
YOLOv8 detects vehicles in each frame.

DeepSORT assigns unique IDs to track each vehicle across frames.

When a vehicle crosses the first line, entry time is recorded.

When it crosses the second line, exit time is recorded, and speed is calculated using:

𝑆
𝑝
𝑒
𝑒
𝑑
=
𝐷
𝑖
𝑠
𝑡
𝑎
𝑛
𝑐
𝑒
𝑇
𝑖
𝑚
𝑒
×
3.6
Speed= 
Time
Distance
​
 ×3.6
The vehicle is counted only once after crossing the exit line.

Bounding boxes display vehicle ID and speed, and the total vehicle count is shown at the top.

📝 Adjustments
Change line_position1 and line_position2 in the code to match your video view.

Adjust real_distance_meters to the actual distance between the two virtual lines for correct speed estimation.

🎥 Sample Output

<img width="1278" height="835" alt="image" src="https://github.com/user-attachments/assets/02ac9308-3a39-414c-997f-b9114334c8f7" />


💡 Future Enhancements
Lane-wise vehicle counting

Average traffic speed analysis

Integration with real-time traffic camera feeds

CSV logging of vehicle ID, speed, and timestamps

📌 Credits
Ultralytics YOLOv8

DeepSORT Realtime
