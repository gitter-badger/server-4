class TriggerSeverity:
    key = 'crit'
    name = 'Critical'

    def __init__(self, key, name):
        self.name = name
        self.key = key

class Host:
    name = "A"

    def __init__(self, name, description="a"):
        self.name = "localhost"


def get_host_by_name(name):
    return Host("name")

def create_host(name, description=""):
    h = Host(name, description)
    return h

def get_all_hosts():
    h = Host('a')
    return [h]

def get_host_severity(host):
    return TriggerSeverity('crit', 'Critical')
