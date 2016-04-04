import boto3
import argparse

#Function to add a simple Tag to EC2 instances
def tagResources(clientEc2,tag,resourcesList):
        for resource in resourcesList:
            response = client.create_tags(DryRun=False,
		Resources=[resource],
		Tags=[{
			'Key': 'name',
			'Value': tag
                        },])
        print "tag name:"+ tag + "is done"
	
#Basic launching of instances
def launchInstances(clientEc2,nbInstances,keyName,securityGroup):
	if nbInstances > 10:
		print "Downscaling number of instances for security"
		nbInstances = 10
	
	print "Launching " + str(nbInstances) + " instances"	
#Launching instance with Basic AWS Linux AMI
	response = clientEc2.run_instances(DryRun=False,
	ImageId='ami-31328842',
	MinCount=nbInstances,
	MaxCount=nbInstances,
	SecurityGroups=[securityGroup],
	KeyName=keyName,
	InstanceType='t2.micro',
	Monitoring={'Enabled': False})

	instances = response['Instances']

	#List of instances id for reuse
	instanceList = []
	#Iteration over the list of instances
	for instance in instances:
		print "InstanceId: "+ instance['InstanceId'] + " is launched"
		instanceList.append(instance['InstanceId'])
	#Returning instances id's
	return instanceList

if __name__ == '__main__':

	#Parsing arguments from CLI
	parser = argparse.ArgumentParser(description='Python program for creating dev environments')
	parser.add_argument('--instances',action="store",type=int ,dest="nbInstances",help='Number of instances you want to create')
	parser.add_argument('--keyName',action="store",type=str, dest="keyName",help="KeyName with which you want to connect")
	parser.add_argument('--sg',action="store",type=str,dest="securityGroup",help="SecurityGroup you want to launch your instances")
	parser.add_argument('--tag',action="store",type=str,dest="tag",help="Tag you want to apply to your resources")

	#Storing arguments CLI into variables
	results = parser.parse_args()

	nbInstances = results.nbInstances
	keyName = results.keyName
	securityGroup = results.securityGroup
	tag = results.tag


	#Client connection
	client = boto3.client('ec2')
        #Launching instances
	instancesList = launchInstances(client,nbInstances,keyName,securityGroup)
	#Tagging instances for later retrieving
	tagResources(client,tag,instancesList)
	
