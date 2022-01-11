from fer import FER
import matplotlib.pyplot as plt


def checkEmotion():
    test_image_one = plt.imread("Images/image.jpg")
    emo_detector = FER(mtcnn=True)
    dominant_emotion, emotion_score = emo_detector.top_emotion(test_image_one)

    return dominant_emotion

