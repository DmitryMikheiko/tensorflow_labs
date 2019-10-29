import tensorflow as tf
import os
from PIL import Image

def show_list_info(l):
    print('Images: ',len(l))
    for i in range(len(l)): 
        print(l[i])
def reduce_img(in_path, out_path,koef = 2):
    img = Image.open(in_path)
    size = img.size
    (width, height) = (img.width // koef, img.height // koef)
    img = img.resize((width, height),resample=Image.NEAREST)
    img.save(out_path,"JPEG",quality=50)
    print("Reduced: " + out_path)
    return size
def restore_img(in_path, out_path, size):
    img = Image.open(in_path)
    img = img.resize(size,resample=Image.NEAREST)
    img.save(out_path,"JPEG",quality=95)
    print("Restored: " + out_path)
def resize_imgs(img_list, img_out_dirs, resize_koef):
    for k in range(len(resize_koef)):
        for path in img_list:
            reduced_img_path = img_out_dirs[k] + os.path.basename(path)
            restored_img_path = img_out_dirs[k] + "res\\" + os.path.basename(path)
            size = reduce_img(path,reduced_img_path,resize_koef[k])
            restore_img(reduced_img_path,restored_img_path,size)
            original_img = tf.image.decode_jpeg(open(path, 'rb').read())
            restored_img = tf.image.decode_jpeg(open(restored_img_path, 'rb').read())
            psnr1 = tf.image.psnr(original_img, restored_img, max_val=255)
           
if __name__ == '__main__':

    resize_koef = [2,4,8,16,32]
    img_list = []
    img_dir = ".\\img"
    img_out_dirs = []
    img_restored_dirs = []
    os.chdir(img_dir)
    #create output directories
    for k in resize_koef:
        path = ".\\out_"+str(k)+"\\"
        path_r = path + "\\res\\"
        img_out_dirs.append(path)
        img_restored_dirs.append(path_r) 
        try:
            os.mkdir(path)
        except FileExistsError:
            pass
        try:
            os.mkdir(path_r)
        except FileExistsError:
            pass
        
    #find jpg images and create list
    base_dir = os.getcwd()+"\\"
    for img in os.listdir():
        if img.endswith('.jpg'):
            img_list.append(base_dir + img)
    #resize images and save

    resize_imgs(img_list, img_out_dirs, resize_koef)  
   
    #show_list_info(img_list)
