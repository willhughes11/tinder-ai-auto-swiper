import cv2
import numpy as np
from deepface import DeepFace
from collections import Counter


class FacialRecognition:
    def identify_faces(self, pil_image):
        image = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        faceCascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
        )
        faces = faceCascade.detectMultiScale(
            gray,
            scaleFactor=1.2,
            minNeighbors=5,
            minSize=(30, 30),
            flags=cv2.CASCADE_SCALE_IMAGE,
        )

        cropped_images = []
        for x, y, w, h in faces:
            cropped_img = image[y : y + h, x : x + w]
            cropped_images.append(cropped_img)

        resized_images = []
        for image in cropped_images:
            resized_image = cv2.resize(image, dsize=(200, 200))
            resized_images.append(resized_image)

        return resized_images

    def match_photos(self, matches):
        for i in range(len(matches)):
            for x in range(len(matches)):
                if not matches[x]["matched"]:
                    result = DeepFace.verify(
                        matches[i]["image"],
                        matches[x]["image"],
                        enforce_detection=False,
                    )
                    if result["verified"]:
                        if matches[i]["matched"]:
                            matches[x]["matched"] = True
                            matches[x]["matched_photo"] = matches[i]["matched_photo"]
                            break
                        else:
                            if i == 0:
                                matches[x]["matched"] = True
                                matches[x][
                                    "matched_photo"
                                ] = f'image_{matches[i]["image_id"]}'
                            else:
                                if matches[i]["image_id"] != matches[x]["image_id"]:
                                    matches[x]["matched"] = True
                                    matches[x][
                                        "matched_photo"
                                    ] = f'image_{matches[i]["image_id"]}'

        return matches

    def compare_faces(self, images):
        matches = []
        z = 0
        for image in images:
            matches.append(
                {"image": image, "image_id": z, "matched": False, "matched_photo": None}
            )
            z += 1

        matches = self.match_photos(matches)
        recurrent_face = Counter(match["matched_photo"] for match in matches)
        most_common = recurrent_face.most_common(1)[0][0]
        filtered_matches = list(
            filter(lambda d: d["matched_photo"] in [most_common], matches)
        )

        images = []
        for i in filtered_matches:
            images.append(i["image"])

        return images

    def analyze_images(self, images):
        analyzed = []
        for image in images:
            obj = DeepFace.analyze(image, actions=["race"], enforce_detection=False)
            analyzed.append(obj)

        dominant_race = Counter(face["dominant_race"] for face in analyzed)
        most_common = dominant_race.most_common(1)[0][0]

        return most_common
