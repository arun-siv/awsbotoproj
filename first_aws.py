import boto3
session = boto3.session.Session()
ec2_console = session.resource(service_name="ec2")
# print(dir(ec2_console))
InstanceId = input("Enter the Instance Id: ")
my_instance = ec2_console.Instance(id=InstanceId)
print(my_instance.state)

