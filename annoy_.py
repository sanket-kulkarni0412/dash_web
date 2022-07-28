
from annoy import AnnoyIndex
import os
import numpy as np
from keras_facenet import FaceNet
from PIL import Image
import pickle

embedder = FaceNet()
image_names= open('image_names','rb')
loaded_list=pickle.load(image_names)
image_names.close()
u = AnnoyIndex(512, 'euclidean')
u.load('test1.ann')
def out_put_of_images(img_path):
    final_img=[]
    x = np.array([np.array(Image.open(img_path))])
    print(x.shape)
    detections = embedder.extract(x[0],threshold=0.95)
    embeddings = list(detections[0].values())[3]
    # tic = time.time()
    neighbours = u.get_nns_by_vector(embeddings, 6)
    # toc = time.time()
    for i in neighbours:
        image_names  = loaded_list[i]
        # print("file path of index {} is {}".format(i, image_names))
        # show_img = Image.open(image_names)
        # show_img
        # fig=plt.figure()
        # fig.add_subplot(1,1,1)
        # plt.axis('off')                                                                                                   
        # plt.imshow(show_img)
        # plt.show()
        final_img.append(image_names)
    return final_img
# neighbours=out_put_of_images('images\\5e62d59413eb0aead86c0254508167e2.jpg')

# for img in final_img:
#   cv2.imshow('img',img)
#   cv2.waitKey(0)