import cv2
from .gaze_tracking import GazeTracking
from typing import List

gaze = GazeTracking()

def analyze_gaze(video_path:str, output_path:str)->List[str]:
    # video_path = 'minute.mp4'
    video_capture = cv2.VideoCapture(video_path)


    # 영상 저장 설정
    output_path = 'output2.mp4'
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    fps = int(video_capture.get(cv2.CAP_PROP_FPS))
    frame_width = int(video_capture.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(video_capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
    out = cv2.VideoWriter(output_path, fourcc, fps, (frame_width, frame_height))

    unstable_gaze_count = 0
    tracking_started = False
    blink_count = 0

    text0 = ""
    text1 = ""
    text2 = ""
    text3 = ""

    right = 0
    left = 0

    # 영상의 총 프레임 수
    total_frames = int(video_capture.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = int(video_capture.get(cv2.CAP_PROP_FPS))

    video_length_seconds = total_frames / fps  # 영상 총 길이

    result = []

    # 30초에 해당하는 프레임 수 (30초동안 눈 10회 이상 깜빡이는지 보려고. 사람 평균이 1분에 20회라고 함)
    frames_per_30sec = 12

    while True:
        # 프레임 읽기
        ret, frame = video_capture.read()

        # 모든 프레임을 읽었을 때 종료
        if not ret:
            break

        # GazeTracking을 사용하여 프레임 분석
        gaze.refresh(frame)

        frame = gaze.annotated_frame()
        text = ""

        if gaze.is_blinking():
            text = "Blinking"
            blink_count += 1



        elif gaze.is_right() or gaze.is_left():
            if not tracking_started:
                tracking_started = True
            unstable_gaze_count += 1
            text = "Looking right" if gaze.is_right() else "Looking left"

            if gaze.is_right():
                right += 1
            elif gaze.is_left():
                left += 1

        elif gaze.is_center():
            text = "Looking center"

        if tracking_started and unstable_gaze_count >= 6:
            text0 = "시선이 불안정합니다"
            # cv2.putText(frame, "Unstable gaze", (90, 190), cv2.FONT_HERSHEY_DUPLEX, 0.9, (147, 58, 31), 1)

        cv2.putText(frame, text, (90, 60), cv2.FONT_HERSHEY_DUPLEX, 1.6, (147, 58, 31), 2)

        left_pupil = gaze.pupil_left_coords()
        right_pupil = gaze.pupil_right_coords()
        cv2.putText(frame, "Left pupil:  " + str(left_pupil), (90, 130), cv2.FONT_HERSHEY_DUPLEX, 0.9, (147, 58, 31), 1)
        cv2.putText(frame, "Right pupil: " + str(right_pupil), (90, 165), cv2.FONT_HERSHEY_DUPLEX, 0.9, (147, 58, 31),
                    1)

        # 경과 시간 계산
        elapsed_frames = int(video_capture.get(cv2.CAP_PROP_POS_FRAMES))  # 경과 프레임 수
        elapsed_seconds = elapsed_frames / fps  # 경과 초

        if elapsed_seconds > video_length_seconds - 5:
            blink_rate_in_30sec = blink_count / (elapsed_seconds / 30)
            if blink_rate_in_30sec > frames_per_30sec:
                # 눈 깜빡임 횟수가 frames_per_minute보다 크면 "눈을 자주 깜빡입니다!" 메시지 출력
                text1 = "눈 깜빡임이 잦습니다"

            else:
                text1 = "눈 깜빡임이 적당합니다"

            if right // unstable_gaze_count > (2 / 3):
                text3 = "오른쪽으로 시선이 치우쳐집니다"


            elif left // unstable_gaze_count > (2 / 3):
                text3 = "왼쪽으로 시선이 치우쳐집니다"

            rate = blink_rate_in_30sec / 10
            # text2 = f'My blink frequency compared to the average person:{rate}'
            text2 = rate

            # cv2.putText(frame, text1, (90, 480), cv2.FONT_HERSHEY_DUPLEX, 0.9, (0, 0, 255), 1)
            # cv2.putText(frame, text2, (90, 530), cv2.FONT_HERSHEY_DUPLEX, 0.9, (0, 0, 255), 1)
            # cv2.putText(frame, text3, (90, 580), cv2.FONT_HERSHEY_DUPLEX, 0.9, (0, 0, 255), 1)

        cv2.imshow("Demo", frame)

        # 1분 동안의 눈 깜빡임 횟수 확인
        if cv2.waitKey(1) == 28:
            break

    # 출력 영상 닫기
    result = [text0, text1, text2, text3]
    out.release()
    video_capture.release()
    cv2.destroyAllWindows()

    return result
