from bottle import route, run, template, debug
import json
from pymongo import MongoClient
from collections import OrderedDict

client = MongoClient('localhost', 27017)
db = client.paranuara


@route('/')
def index():
    return template('<h2><b>Welcome to the {{name}} API</b></h2>.', name='Paranuara')


@route('/company/<cname>')  # <cname:re:[\w ]+>
def get_companies(cname):
    '''
    Function to GET the name of employees working in a certain company
    :param cname: Company name
    :return: Employees in the company
    '''
    if not cname:
        message = 'Missing mandatory field : Company name'
    else:
        emp_company = db.companies.find_one({'company': cname}, {'index': 1})
        if not emp_company:
            message = 'No company found with the name \'' + cname + '\''
        else:
            # emp_index_list = [emp['index'] for emp in emp_company]
            employees = db.people.find({'company_id': emp_company['index']}, {'name': 1, 'age': 1, 'index': 1,
                                                                              'email': 1, 'phone': 1, '_id': 0})
            if employees.count() < 1:
                message = 'No employee found in the company \'' + cname + '\''
            else:
                message = str(json.dumps(list(employees)))
    return template('{{message}}', message=message)


@route('/people/<p1>/<p2>', method='GET')
def get_friends(p1, p2):
    '''
    Function to GET the details of two person and their mutual friends
    :param p1: Person 1 index in people collection
    :param p2: Person 1 index in people collection
    :return: name, age, address, phone, friends and their alive mutual friends with brown eyes
    '''
    if not p1:
        message = 'Missing mandatory field : Person1 index'
    elif not p2:
        message = 'Missing mandatory field : Person2 index'
    elif not (p1.isdigit() and p2.isdigit()):
        message = 'Person1 and Person 2 indices should be integer.'
    else:
        twop = db.people.find({'index': {'$in': [int(p1), int(p2)]}},
                           {'name': 1, 'age': 1, 'address': 1, 'phone': 1, 'friends': 1, '_id': 0})
        if twop.count() == 0:
            message = 'Details for both the people not found. Please pass correct index.'
        elif twop.count() == 1:
            # not_found = p2 if a[0]['index'] == p1 else p1
            message = 'Details for one of the person not found. Please pass correct index.'
        else:
            a_friends = set([friend['index'] for friend in twop[0]['friends']])
            b_friends = set([friend['index'] for friend in twop[1]['friends']])
            common = list(a_friends & b_friends)
            message = ''
            for people in twop:
                del people['friends']
                message += 'Person : ' + json.dumps(people)
            # message_list = list(twop)
            commonf = db.people.find({'eyeColor': 'brown', 'has_died': False, 'index': {'$in': common}}, {'name': 1,
                                                      'age': 1, 'index': 1, 'email': 1, 'phone': 1, '_id': 0})
            message += ' Common alive brown-eyed friends : ' + str(json.dumps(list(commonf)))
    return template('{{message}}', message=message)


@route('/choice/<index>', method='GET')  # <cname:int>
def get_food_liking(index):
    '''
    Function to GET the username, age and food choices from user index
    :param index: Index of the person in people collection
    :return: JSON: {"username": "Dummy", "age": 25, "fruits": ["abc"], "vegetables": ["xyz"]}
    '''
    if not index:
        message = 'Missing mandatory field : Name of the person'
    else:
        emp_liking = db.people.find_one({'index': int(index)}, {'name': 1, 'age': 1, 'favouriteFood': 1, '_id': 0})
        if not emp_liking:
            message = 'No person found with the index \'' + index + '\''
        else:
            veggies = ['celery', 'cucumber', 'lettuce', 'beetroot', 'carrot']
            fruits = ['orange', 'apple', 'strawberry', 'banana']
            fav_fruits = []
            fav_veggies = []
            message_dict = OrderedDict()  # To maintain the desired interface
            message_dict['username'] = emp_liking['name']
            message_dict['age'] = emp_liking['age']
            for fav in emp_liking['favouriteFood']:
                if fav in veggies:
                    fav_fruits.append(fav)
                elif fav in fruits:  # anticipating options which are none of veggie or fruit
                    fav_veggies.append(fav)
            del emp_liking
            message_dict['fruits'] = fav_fruits
            message_dict['vegetables'] = fav_veggies
            message = json.dumps(message_dict)
    return template('{{message}}', message=message)


# debug(True)
if __name__ == '__main__':
    run(host='localhost', port=9090)
