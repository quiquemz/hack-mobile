from flask import Flask
from flask import jsonify
import pickle

app = Flask(__name__)

def app_run():
    app.run(host = '127.0.0.1', port = 5000)

def save_obj(obj, name):
    with open('obj/'+ name + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

def load_obj(name):
    with open('obj/' + name + '.pkl', 'rb') as f:
        return pickle.load(f)

def wash_object(id_tag):
    wash_time = time.strftime('%m/%d/%Y')
    load_list = load_obj(id_tag)
    load_list[4] = wash_time
    load_list[5] = 0
    save_obj(load_list, id_tag)

@app.route('/get-current-wear')
def get_current_wear():
    return jsonify((load_obj('current'))['list'])

@app.route('/get-wardrobe')
def get_wardrobe():
    return jsonify((load_obj('wardrobe')))

def get_type_list(cat):
    wardrobe = load_obj('wardrobe')
    ret_list = []
    for id_tag in wardrobe:
        item = load_obj(id_tag)
        if (item['type']).lower() == cat.lower():
            ret_list.append(item)
    return ret_list

@app.route('/get-category/<cat>')
def get_category(cat):
    return jsonify(get_type_list(cat))


@app.route('/get-all-clothes')
def get_all_clothes():
    ret_list = []
    ret_list.append(get_type_list('Shirts'))
    ret_list.append(get_type_list('Pants'))
    ret_list.append(get_type_list('Shoes'))
    return jsonify(ret_list)

@app.after_request
def after_request(response):
  response.headers.add('Access-Control-Allow-Origin', '*')
  response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
  response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
  return response


obj_list = {'imgUrl' : 'img1', 'name' : "J.Crew Cotton Shirt", 'type' :"Shirts",'debut': "21/03/2016",'timesWorn' : 5,'lastWash' :"07/01/2016", 'dirtyDays' : 3}
obj_list2 = {'imgUrl' : 'img2', 'name' : "Gap Shirt", 'type' :"Shirts",'debut': "01/03/2016",'timesWorn' : 4,'lastWash' :"07/01/2016", 'dirtyDays' : 7}
obj_list3 = {'imgUrl' : 'img1', 'name' : "Nike Pants ", 'type' :"Pants",'debut': "21/03/2016",'timesWorn' : 8,'lastWash' :"07/01/2016", 'dirtyDays' : 3}
obj_list4 = {'imgUrl' : 'img2', 'name' : "Converse Shoes", 'type' :"Pants",'debut': "14/12/2016",'timesWorn' : 9,'lastWash' :"07/01/2016", 'dirtyDays' : 8}
obj_list5 = {'imgUrl' : 'img1', 'name' : "Alden Shoes", 'type' :"Shoes",'debut': "21/09/2016",'timesWorn' : 1,'lastWash' :"07/01/2016", 'dirtyDays' : 6}
save_obj(obj_list, str(1))
save_obj(obj_list2, str(2))
save_obj(obj_list3, str(3))
save_obj(obj_list4, str(4))
save_obj(obj_list5, str(5))
save_obj(['1','2','3','4','5'],'wardrobe')
save_obj({'time' : "07/08/2017", 'list' : ['7', '6', '2']}, 'current')

app_run()
