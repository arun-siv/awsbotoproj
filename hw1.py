import boto3
import sys

def future_state():
  if len(sys.argv) !=2 :
    raise SystemExit("Usage of the Script should be python <script.py> start | stop")
  required_state = sys.argv[1]
  return required_state


def process_state_change(instance , current_state_ec2, future_state_ec2):
  ''' State change given an instance object  '''
  if current_state_ec2 == 'running' and future_state_ec2 == 'stop':
      instance.stop()
  elif current_state_ec2 == 'stopped' and future_state_ec2 == 'start':
    instance.start()


if __name__ == '__main__':
  session = boto3.Session()
  ec2_console = session.resource(service_name="ec2")
  # instanceids = ["i-0c628135af43e64a4","i-0c628135af43e64a4"]
  fl2 = {'Name': 'tag:Image','Values': ['Linux']}
  myinstances = ec2_console.instances.filter(
                Filters=[fl2],
                # InstanceIds=instanceids
                )

  for instance in myinstances:
    # print(instance)
    current_state_ec2 = instance.state['Name']
    future_state_ec2 = future_state()
    process_state_change(instance, current_state_ec2 , future_state_ec2)
    print(f"The instance state changed has been done successfully for {instance.id}")



