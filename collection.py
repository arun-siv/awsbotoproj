import boto3
session = boto3.Session()
ec2_console = session.resource(service_name='ec2')
for i in ec2_console.instances.all() :
  print(f"{i.instance_id},{i.instance_type}")


ec2_client = session.client(service_name="ec2")

inst_details = [ (i["InstanceId"],i["InstanceType"])
               for j in  ec2_client.describe_instances()['Reservations']
               for i in j['Instances']
              ]

inst_1 = (
          j for  i in ec2_client.describe_instances()['Reservations']
          for j in i['Instances']
         )

