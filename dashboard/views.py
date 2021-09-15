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
}

obj = {}
gtw1 = {}
gtw2 = {}
gtw3 = {}

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
        return

    status = con.api(options['status']).getBody()

    obj['isconected'] = 'OK'
    obj['since'] = getUpTime(status)
    obj['sessions'] = getSessions(status)
    obj['max_sessions'] = getmMaxsessions(status)
    obj['stack_size'] = getStackSize(status)
    obj['stack_min_size'] = getMinStackSize(status)

    gtw_status = con.api(options['status_gateway_ms1']).getBody()
    gtw1['name'] = getName(gtw_status)
    gtw1['status'] = getGtwStatus(gtw_status)
    gtw1['since'] = getSinceGtw(gtw_status)
    gtw1['callin'] = getCallIn(gtw_status)
    gtw1['callin_fail'] = getCallInFail(gtw_status)
    gtw1['callout'] = getCallOut(gtw_status)
    gtw1['callout_fail'] = getCallOutFail(gtw_status)

    gtw_status = con.api(options['status_gateway_ms2']).getBody()
    gtw2['name'] = getName(gtw_status)
    gtw2['status'] = getGtwStatus(gtw_status)
    gtw2['since'] = getSinceGtw(gtw_status)
    gtw2['callin'] = getCallIn(gtw_status)
    gtw2['callin_fail'] = getCallInFail(gtw_status)
    gtw2['callout'] = getCallOut(gtw_status)
    gtw2['callout_fail'] = getCallOutFail(gtw_status)

    gtw_status = con.api(options['status_gateway_ms2']).getBody()
    gtw3['name'] = getName(gtw_status)
    gtw3['status'] = getGtwStatus(gtw_status)
    gtw3['since'] = getSinceGtw(gtw_status)
    gtw3['callin'] = getCallIn(gtw_status)
    gtw3['callin_fail'] = getCallInFail(gtw_status)
    gtw3['callout'] = getCallOut(gtw_status)
    gtw3['callout_fail'] = getCallOutFail(gtw_status)

    print(gtw3)
    return render(request, 'dashboard/dashboard.html', {'obj': obj, 'gtw1': gtw1, 'gtw2': gtw2, 'gtw3': gtw3})


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
    return gtw_status.split('\n')[2].split('\t')[1]
