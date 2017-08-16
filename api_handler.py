from bottle import redirect, request, route, run, template, debug
import json
from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client.paranuara


@route('/')
def index():
    return template('<b>Welcome to the {{name}} API</b>!', name='Paranuara')


@route('/company/<cname>')  # <cname:re:[\w ]+>
def get_companies(cname):
    if not cname:
        message = 'Missing mandatory field : Company name'
    emp_company = db.companies.find({'company': cname})
    if emp_company.count() < 1:
        message = 'No employee found in the company \'' + cname + '\''
    else:
        emp_index_list = [emp['index'] for emp in emp_company]
        employees = db.people.find({'index': {'$in': emp_index_list}})
        if employees.count() < 1:
            message = 'Employee details not found in the database.'
        elif employees.count() == 1:
            message = json.dumps((employees.next()))
        else:
            message = str(list(employees))
    return template('{{message}}', message=message)


@route('/people/<names>', method='GET')
def get_friends():
    p1 = request.GET.get('p1', '').strip()
    p2 = request.GET.get('p2', '').strip()
    if not p1 or not p2:
        message = 'Missing mandatory field : Person1 index'
    elif not p2:
        message = 'Missing mandatory field : Person2 index'
    else:
        a = db.people.find({'index': {'$in': [p1, p2]}},
                           {'name': 1, 'age': 1, 'address': 1, 'phone': 1, 'friends': 1, '_id': 0})
        a_friends = set([friend['index'] for friend in a[0]['friends']])
        b_friends = set([friend['index'] for friend in a[1]['friends']])
        common = list(a_friends & b_friends)
        message_list = list(a)
        b = db.people.find({'eyeColor': 'brown', 'has_died': False, 'index': {'$in': common}})
        message_list.append(list(b))
        message = str(message_list)
    return template('{{message}}', message=message)


@route('/choice/<pname>', method='GET')  # <cname:int>
def get_food_liking(pname):
    if not pname:
        message = 'Missing mandatory field : Name of the person'
    emp_liking = db.people.find_one({'name': pname}, {'name': 1, 'age': 1, 'favouriteFood': 1, '_id': 0})
    if not emp_liking:
        message = 'No person found with the name \'' + pname + '\''
    veggies = ['celery', 'cucumber', 'lettuce', 'beetroot', 'carrot']
    fruits = ['orange', 'apple', 'strawberry', 'banana']
    fav_fruits = []
    fav_veggies = []
    for fav in emp_liking['favouriteFood']:
        if fav in veggies:
            fav_fruits.append(fav)
        elif fav in fruits:  # anticipating options which are none of veggie or fruit
            fav_veggies.append(fav)
    del emp_liking['favouriteFood']
    emp_liking['fruits'] = fav_fruits
    emp_liking['vegetables'] = fav_veggies
    message = json.dumps(emp_liking)
    return template('{{message}}', message=message)

debug(True)
if __name__ == '__main__':
    run(host='localhost', port=9090)