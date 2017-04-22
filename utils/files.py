def write_to_file(name, data):
    f = open(name, 'w')
    f.write(data)


def read_file(name):
    f = open(name, 'r')
    data = f.read().split('\n')
    return data
