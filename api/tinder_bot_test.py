from PIL import Image
import requests
from services.utility_functions import open_json_file
from services.facial_recognition import FacialRecognition
from services.attractiveness_rating import Attractiveness_Rating
import numpy as np

fr = FacialRecognition()
ar = Attractiveness_Rating()
output = open_json_file('test_matches.json')
for i in output:
    for x in i['data']['results']:
        print(x['user']['name'])
        print('-'*100)

        all_faces = []
        for y in x['user']['photos']:
            img_url = y['processedFiles'][0]['url']
            try:
                im = Image.open(requests.get(img_url, stream=True).raw).convert('RGB')
            except:
                im = None

            if im:
                identified_faces = fr.identify_faces(im)
                all_faces.append(identified_faces)

        arr = []
        for i in all_faces:
            for x in i:
                arr.append(x)

        if len(arr) > 0:
            compared_faces = fr.compare_faces(arr)
            analayzed_faces = fr.analyze_images(compared_faces)
            print(analayzed_faces)
            ratings = ar.attractiveness_rating(compared_faces)
            print(np.average(ratings))
        # vertical = np.concatenate(compared_faces, axis=0)
        # cv2.imshow('VERTICAL', vertical)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()
    #     break
    # break