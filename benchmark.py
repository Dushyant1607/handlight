import cv2
import time
import argparse
from hand_tracker import HandTracker


def run_benchmark(num_frames=200):
    cap = cv2.VideoCapture(0)
    tracker = HandTracker()

    detected = 0
    total = 0
    latencies = []

    print(f"[BENCHMARK] Running for {num_frames} frames...")
    print(f"[BENCHMARK] Show your hand to the camera...")

    while total < num_frames:
        success, frame = cap.read()
        if not success:
            continue

        frame = cv2.flip(frame, 1)
        total += 1

        start = time.perf_counter()
        frame = tracker.find_hands(frame, draw=True)
        landmarks = tracker.get_landmark_positions(frame)
        elapsed = (time.perf_counter() - start) * 1000

        latencies.append(elapsed)

        if len(landmarks) >= 9:
            detected += 1

        cv2.putText(frame, f"Frame: {total}/{num_frames}",
                    (10, 30), cv2.FONT_HERSHEY_SIMPLEX,
                    0.8, (0, 255, 0), 2)
        cv2.putText(frame, f"Detected: {detected}",
                    (10, 65), cv2.FONT_HERSHEY_SIMPLEX,
                    0.8, (0, 255, 200), 2)
        cv2.imshow("Benchmark", frame)

        if cv2.waitKey(1) & 0xFF == 27:
            break

    cap.release()
    cv2.destroyAllWindows()

    accuracy = detected / total * 100
    avg_latency = sum(latencies) / len(latencies)

    print(f"\n--- Results ---")
    print(f"Frames tested  : {total}")
    print(f"Hands detected : {detected}")
    print(f"Accuracy       : {accuracy:.1f}%")
    print(f"Avg latency    : {avg_latency:.1f} ms/frame")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--frames", type=int, default=200)
    args = parser.parse_args()
    run_benchmark(args.frames)