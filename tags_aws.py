import boto3
#x77nD&g2!VM(xtZ@XfP&FS-dSmZT&Y@$

session = boto3.session.Session()

ec2_console = session.resource(service_name="ec2")

id = "i-0c628135af43e64a4"

my_instance = ec2_console.Instance(id)
''
print(my_instance.tags)

current_state = my_instance.state['Name']

if current_state == 'stopped' :
  print(f"the instance {id} is in stopped state")
  print(f"Starting the instance {id}")
  my_instance.start()
  my_instance.wait_until_running()

if current_state == 'running' :
  print(f"the instance {id} is in running state")
  print(f"Stopping the instance {id}")
  my_instance.stop()
  my_instance.wait_until_stopped()
