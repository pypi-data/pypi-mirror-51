import video_process as vp
import image_process as ct 
import image_reco as reco
import text_process as txt
import cv2


def main():

# =================== 동영상 테스트 ================================
    fianl_result_array=[]
    section_result_array=[]

    video_path='input/baek.mp4'
    # video에서 프레임 추출 
    frame_images = vp.extract_frame_from_video(video_path)
    # 추출된 프레임에서 글자 영역 찾기 
    for i, frame in enumerate(frame_images):
        vp.save_image(frame,i)
        final_result=[]
        copy = ct.resize(frame)
        cropped_images=ct.image_all_process(copy)
        num =0 
        # 한 프레임의 글자 영역들의 텍스트 추출 
        # 자막들 
        for con in cropped_images["contours"]:
            # 프레임에서 추출한 영역들 저장 
            ct.save_crooped_contours(con, 'frame_{}_contours_{}'.format(i , num))
            # 영역들에서 글자 추출 
            result = reco.extract_text(con)
            # 추출된 글자 전처리 후 임시 보관 
            tmp = txt.text_pre_process(result)
            if (tmp is not None) :
                final_result.append(tmp)
            # final_result.append(result)

            num+=1
        # 한 프레임 씩 배열에 저장 
        fianl_result_array.append(final_result)

        # 섹션 
        # 섹션 영역 저장 
        ct.save_crooped_contours(cropped_images["section"], 'section_{}'.format(i))
        # 섹션에서 글자 추출 
        section = reco.extract_text(cropped_images["section"])
        # 추출된 글자 전처리 후 저장 
        section_result_array.append(txt.text_pre_process(section))
        # section_result_array.append(section)

    # 모든 결과 값들 저장 하기 
    txt.text_save(fianl_result_array, section_result_array, 'output/baek/baek.csv')

# def vision_test(path):
#     """Detects text in the file."""
#     from google.cloud import vision
#     client = vision.ImageAnnotatorClient()

#     with io.open(path, 'rb') as image_file:
#         content = image_file.read()

#     image = vision.types.Image(content=content)

#     response = client.text_detection(image=image)
#     texts = response.text_annotations
#     print('Texts:')

#     for text in texts:
#         print('\n"{}"'.format(text.description))

#         vertices = (['({},{})'.format(vertex.x, vertex.y)
#                     for vertex in text.bounding_poly.vertices])

#         print('bounds: {}'.format(','.join(vertices)))

    # import io
    # import os

    # # Imports the Google Cloud client library
    # from google.cloud import vision
    # from google.cloud.vision import types

    # # Instantiates a client
    # client = vision.ImageAnnotatorClient()

    # # The name of the image file to annotate
    # file_name = os.path.join(
    #     os.path.dirname(__file__),
    #     'resources/wakeupcat.jpg')

    # # Loads the image into memory
    # with io.open(file_name, 'rb') as image_file:
    #     content = image_file.read()

    # image = types.Image(content=content)

    # # Performs label detection on the image file
    # response = client.label_detection(image=image)
    # labels = response.label_annotations

    # print('Labels:')
    # for label in labels:
    #     print(label.description)

if __name__ == "__main__":
    main()
    # vision_test('output/frames/frame308.jpg')