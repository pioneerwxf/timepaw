from timepaw.activekeys.models import ActiveKey
from django.http import HttpResponse

def add(request):
    key = request.GET['keyv']
    ActiveKey.objects.create(key = key)
    msg = "key :: %s added." % (key)
    return HttpResponse(msg)

def use(key):
    if ActiveKey.objects.filter(key = key):
        if not ActiveKey.objects.get(key = key).used:
            ActiveKey.objects.get(key = key).used = True
            return True
    return False