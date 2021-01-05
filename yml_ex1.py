import yaml
def ec2_filter_file(filename):
  with open(filename) as f:
    result = yaml.load(f)
    # filter_list = []
    # for k,v in result.items():
    #   filter_map = dict()
    #   filter_map['Name'] = k
    #   filter_map['Values'] = v
    #   filter_list.append(filter_map)
    # return filter_list
    return [{'Name':k,'Values':v} for k,v in result.items()]

if __name__ == '__main__':
  pass
