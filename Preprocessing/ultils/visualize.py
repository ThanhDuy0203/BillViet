import matplotlib
matplotlib.rc('font', family= 'TakaoPGothic')
from matplotlib import pyplot as plt

import matplotlib.patches as patches
import cv2, os, csv
from ultils.common_ import poly, get_list_file_in_folder, get_list_gt_poly, type_map

color_map = {1: 'green', 15: 'red', 16: 'blue', 17: 'm', 18: 'cyan'}
txt_color_map = {1: 'green', 15: 'red', 16: 'blue', 17: 'm', 18: 'cyan'}
inv_type_map = {v: k for k, v in type_map.items()}


def viz_poly(img, list_poly, save_viz_path= None, ignor_type= [1]):
    fig, ax = plt.subplots(1)
    fig.set_size_inches(20, 20)
    plt.imshow(img)
    
    for polygon in list_poly:
        ax.add_patch(
            patches.Polygon(polygon.list_pts, linewidth= 2, edgecolor= color_map[polygon.type], facecolor= None))
        draw_value= polygon.value 
        if polygon.type in ignor_type:
            draw_value= ''
            plt.text(polygon.list_pts[0][0], polygon.list_pts[0][1], draw_value, fontsize= 20,
                     fontdict={'color':txt_color_map[polygon.type]})
    
    if save_viz_path is not None:
        print('Save visualize result to', save_viz_path)
        fig.savefig(save_viz_path, bbox_inches= 'tight')
        
def viz_icdar(img_path, anno_path, save_viz_path= None, extract_kie_type= False, ignor_type= [1]):
    if not isinstance(img_path, str):
        image= img_path
    else:
        image= cv2.imread(img_path)
        image= cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        
    list_poly = []
    with open(anno_path, 'r', encoding='utf-8') as f:
        anno_txt= f.readlines()
        
    for anno in anno_txt:
        anno = anno.rstrip('\n')
        
        idx= -1
        for i in range(0, 8):
            idx= anno.find(',', idx+1)
            
        coordinates = anno[:idx]
        val= anno[idx+1:]
        type= 1
        
        if extract_kie_type:
            last_comma_idx= val.rfind(',')
            type_str= val[last_comma_idx +1:]
            val= val[:last_comma_idx]
            if type_str in inv_type_map.keys():
                type= inv_type_map[type_str]
                
        coors= [int(f) for f in coordinates.split(',')]
        pol= poly(coors, type=type, value=val)
        list_poly.append(pol)
    viz_poly(img= image,
             list_poly= list_poly,
             save_viz_path= save_viz_path,
             ignor_type= ignor_type)
        
        
        
        
        


if __name__ == '__main__':
    img_path= 'D:\FPTUniversity\Semester 6\BillViet_Prj\test_img\mcocr_val_145114anqqj.jpg'
    anno_path= 
    