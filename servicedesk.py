#!/usr/bin/env python3
import requests
from bs4 import BeautifulSoup

def get_ticket():

    loginurl = 'https://servicedesk.phoenixit.ru/'
    logindata = {'autologin' : '1', 'login' : 'infra', 'password' : 'oHR4]{_sH@[=H38L;L#p', 'enter' : 'submit', 'stateid': '249'}
    headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 5.1; rv:31.0) Gecko/20100101 Firefox/31.0',
            'Content-type' : 'application/x-www-form-urlencoded', 'stateid': '249'}
    session=requests.session()
    login=session.post(loginurl, params=logindata, headers=headers)
    url = 'https://servicedesk.phoenixit.ru/Task'
    soup = BeautifulSoup(session.get(url).content, 'html.parser')

    status = 'Открыта'
    out = {}
    for a in soup.find_all('td', class_='task-statusid'):
        d = {}

        if a.find('img', alt=status):

            taskid = a.find('img', alt=status).get('taskid')
            print ('sd task #: ' + taskid)
            url = loginurl+"Task/view/"+taskid
            soup_view = BeautifulSoup(session.get(url).content, 'html.parser')
            created = soup_view.find('div', class_='created').text
            vm = None
            d.update ({'head':'''================================ \n============ ''' +taskid+
                              ''' ============= \n================================\n'''})
            d.update ({'head_name': 'НАЗВАНИЕ: ' + soup_view.find('input', id='name').get('value') + '\n'})

            if soup_view.find('span', id='tasktypespan').get('title') == 'INFRA_NEW_VM':
                vm = 'HOSTNAME ' + soup_view.find('input', id='field1041').get('value') + '\n'
                vm += 'CPU  ' + soup_view.find('select', id='field1017').find('option', selected="true").text + '\n'
                vm += 'RAM  ' + soup_view.find('select', id='field1014').find('option', selected="true").text + '\n'
                vm += 'HDD  ' + soup_view.find('select', id='field1015').find('option', selected="true").text + '\n'
                vm += 'OS   ' + soup_view.find('select', id='field1016').find('option', selected="true").text + '\n\n'
                d.update({'vm':vm})

            if soup_view.find('span', id='tasktypespan').get('title') == 'Стандартный':
                pass

            if soup_view.find('span', id='tasktypespan').get('title') == 'INFRA_VM_PROBLES':
                vm = 'HOSTNAME ' + soup_view.find('input', id='field1033').get('value') + '\n'
                vm += 'IP ' + soup_view.find('input', id='field1034').get('value')
                d.update({'vm': vm})

            d.update({'description_head' : '\n-_-_-_-_-_-_-_-_ОПИСАНИЕ_-_-_-_-_-_-_-_-'})
            d.update({'Description': soup_view.find("textarea", id='description').text + '\n'})
            d.update({'comment_head': '-_-_-_-_-_-_-_КОМЕНТАРИЙ_-_-_-_-_-_-_-'})
            lifetimeshort = soup_view.find('div', id='lifetimeshort').text.replace("\n\n\n\n", " ")
            d.update ({'comment' : lifetimeshort.replace("\n\n\n", "\n").replace("^\ ", "")})
            d.update ({'created_head':'-_-_-_-_-_-_-_-_-_СОЗДАНА_-_-_-_-_-_-_-_-'})
            d.update ({'created': created.replace('  ', '') + soup_view.find('ul', class_='users').find('a',class_='nounderline').text + '\n'})
            #out.update({ taskid: url + "\n" + d['head'] + d['head_name'] + d['vm'] + d['description_head'] + d['Description'] +
            out[taskid] =  d['head_name'] + d['vm'] + d['description_head'] + d['Description'] + d['comment_head'] + d['comment'] + '\n' + d['created_head'] + d['created']
    return (out)


def send_teleg():

    tickets = get_ticket()
    print (str (tickets) )
    #for key, value in tickets.items():
    #    print ( key )
    #    print ( value )

#send_teleg()
