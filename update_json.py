import json
import argparse
def updata_json(size,dist,ele,azim,obj):
    data = open("json.json", "r")
    json_object = json.load(data)
    data.close()
    json_object["image_size"]  = size
    json_object["camera_dist"] = dist
    json_object["elevation"]   = ele
    json_object["azim_angle"]  = azim
    json_object["obj_filename"] = obj
    data = open("json.json", "w")
    json.dump(json_object, data)
    data.close()
if __name__=="__main__":
    parser = argparse.ArgumentParser(description='test json ')
    parser.add_argument(
        '--size',
        type=int,
        help='value of image size ')
    parser.add_argument(
        '--dist',
        type=int,
        help='value of camera distance  ')
    parser.add_argument(
        '--ele',
        type=int,
        default=0,
        help='value of elevation  ')
    parser.add_argument(
        '--azim',
        type=list,
        default=[0,90,180,270],
        help='value of azim_angle  ')
    parser.add_argument(
        '--obj',
        type=str,
        help='path to object file ')
    args = parser.parse_args()
    size = args.size
    dist = args.dist
    ele  = args.ele
    azim = args.azim
    obj  = args.obj
    updata_json(size,dist,ele,azim,obj)