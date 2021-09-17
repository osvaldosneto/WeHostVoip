from django.shortcuts import render
from freeswitchESL import ESL

options = {
    'auth': 'ClueCon',
    'server': '127.0.0.1',
    'port': '8021',
    'status': 'status',
    'status_gateway_ms1': 'sofia status gateway example.com',
    'status_gateway_ms2': 'sofia status gateway example.com',
    'status_gateway_ms3': 'sofia status gateway example.com',
    'status_default_GTW': 'sofia status gateway example.com',
}

obj = {}
gtw1 = {}
gtw2 = {}
gtw3 = {}
gtw4 = {}

def dashboard(request):
    con = ESL.ESLconnection(options['server'], options['port'], options['auth'])
    con.events('plain', 'all')

    if not con.connected():
        print('Not Connected')
        obj['isconected'] = 'NOK'
        obj['since'] = '0 year, 0 days, 0 hours, 0 minutes'
        obj['sessions'] = '0'
        obj['max_sessions'] = '0'
        obj['stack_size'] = '0'
        obj['stack_min_size'] = '0'
        gtw1 = setGatewayNull()
        gtw2 = setGatewayNull()
        gtw3 = setGatewayNull()
        gtw4 = setGatewayNull()
        return render(request, 'dashboard/dashboard.html', {'obj': obj, 'gtw1': gtw1, 'gtw2': gtw2, 'gtw3': gtw3, 'gtw4' : gtw4})

    status = con.api(options['status']).getBody()
    obj['isconected'] = 'OK'
    obj['since'] = getUpTime(status)
    obj['sessions'] = getSessions(status)
    obj['max_sessions'] = getmMaxsessions(status)
    obj['stack_size'] = getStackSize(status)
    obj['stack_min_size'] = getMinStackSize(status)

    gtw_status = con.api(options['status_gateway_ms1']).getBody()
    if gtw_status.split(' ')[0] != 'Invalid':
        gtw1 = setGateway(gtw_status)
    else:
        gtw1 = setGatewayNull()

    gtw_status = con.api(options['status_gateway_ms2']).getBody()
    if gtw_status.split(' ')[0] != 'Invalid':
        gtw2 = setGateway(gtw_status)
    else:
        gtw2 = setGatewayNull()

    gtw_status = con.api(options['status_gateway_ms3']).getBody()
    if gtw_status.split(' ')[0] != 'Invalid':
        gtw3 = setGateway(gtw_status)
    else:
        gtw3 = setGatewayNull()

    gtw_status = con.api(options['status_default_GTW']).getBody()
    if gtw_status.split(' ')[0] != 'Invalid':
        gtw4 = setGateway(gtw_status)
    else:
        gtw4 = setGatewayNull()

    return render(request, 'dashboard/dashboard.html', {'obj': obj, 'gtw1': gtw1, 'gtw2': gtw2, 'gtw3': gtw3, 'gtw4' : gtw4})


def setGateway(gtw_status):
    gtw = {}
    gtw['name'] = getName(gtw_status)
    gtw['status'] = getGtwStatus(gtw_status)
    gtw['since'] = getSinceGtw(gtw_status)
    gtw['callin'] = getCallIn(gtw_status)
    gtw['callin_fail'] = getCallInFail(gtw_status)
    gtw['callout'] = getCallOut(gtw_status)
    gtw['callout_fail'] = getCallOutFail(gtw_status)
    return gtw


def setGatewayNull():
    gtw = {}
    gtw['name'] = "NULL"
    gtw['status'] = "NULL"
    gtw['since'] = "NULL"
    gtw['callin'] = 0
    gtw['callin_fail'] = 0
    gtw['callout'] = 0
    gtw['callout_fail'] = 0
    return gtw


def getUpTime(status):
    time = status.split('\n')[0]
    strip_caracter = ','
    since_time = strip_caracter.join(time.split(strip_caracter)[:4])
    return since_time[3:len(since_time)]


def getSessions(status):
    return status.split('\n')[2].split(' ')[0]


def getmMaxsessions(status):
    return status.split('\n')[5].split(' ')[0]


def getStackSize(status):
    max_stack = status.split('\n')[7].split(' ')[3].split('/')[1]
    max_stack = max_stack[:-1]
    return max_stack


def getMinStackSize(status):
    min_stack = status.split('\n')[7].split(' ')[3].split('/')[0]
    min_stack = min_stack[:-1]
    return min_stack


def getGtwStatus(gtw_status):
    return gtw_status.split('\n')[20].split('\t')[1]


def getSinceGtw(gtw_status):
    time = gtw_status.split('\n')[21].split('\t')[1][:-1]
    t = convert(int(time)).split(':')
    return str(t[0]) + ' d  ' + str(t[1]) + ' h  ' + str(t[2]) + ' m'


def convert(seconds):
    min, sec = divmod(seconds, 60)
    hour, min = divmod(min, 60)
    day, hour = divmod(hour, 24)
    return "%d:%d:%02d:%02d" % (day, hour, min, sec)


def getCallIn(gtw_status):
    return gtw_status.split('\n')[22].split('\t')[1]


def getCallInFail(gtw_status):
    return gtw_status.split('\n')[24].split('\t')[1]


def getCallOut(gtw_status):
    return gtw_status.split('\n')[23].split('\t')[1]


def getCallOutFail(gtw_status):
    return gtw_status.split('\n')[25].split('\t')[1]


def getName(gtw_status):
    return gtw_status.split('\n')[1].split('\t')[1]
