import boto3
import sys

def future_state():
  if len(sys.argv) !=2 :
    raise SystemExit("Usage of the Script should be python <script.py> start | stop")
  required_state = sys.argv[1]
  return required_state

if __name__ == '__main__':
  session = boto3.Session()
  ec2_console = session.resource(service_name='ec2')
  instanceids = ["i-0c628135af43e64a4","i-0c628135af43e64a4"]
  fl2 = {'Name': 'tag:Image','Values': ['Windows']}
  myinstances = ec2_console.instances.filter(
                Filters=[fl2],
                InstanceIds=instanceids
                )

  my_ec2 = [i.id for i in myinstances]
  if future_state() == 'stop':
    ec2_console.instances.stop(InstanceIds=my_ec2)
    print("All instances stopped!!!")
  elif future_state() == 'start':
    ec2_console.instances.start(InstanceIds=my_ec2)
    print("All instances Started!!!")
