import sys

import boto3

import yml_ex1


def future_state():
  ''' Returns future instance state based on script input'''
  if len(sys.argv) !=2 :
    raise SystemExit("Usage of the Script should be python <script.py> start | stop")
  required_state = sys.argv[1]
  return required_state

if __name__ == '__main__':
  session = boto3.Session()
  ec2_console = session.resource(service_name='ec2')
  ec2_cli = session.client(service_name='ec2')
  #get the filter from yaml config
  fl1 = yml_ex1.ec2_filter_file('conf.yaml')
  #filter the ec2 based on tag
  myinstances = ec2_console.instances.filter(
                Filters=fl1
                 )
  my_ec2 = [i.id for i in myinstances] # list comprehension

  if future_state() == 'stop':
    waiter = ec2_cli.get_waiter('instance_stopped')
    ec2_console.instances.stop(InstanceIds=my_ec2)
    waiter.wait(InstanceIds=my_ec2)
    print("All instances stopped!!!")
    
  elif future_state() == 'start':
    waiter = ec2_cli.get_waiter('instance_running')
    ec2_console.instances.start(InstanceIds=my_ec2)
    print("All instances Started!!!")
    waiter.wait(InstanceIds=my_ec2)
