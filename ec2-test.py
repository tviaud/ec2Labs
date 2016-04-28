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

def terminateInstancesByTag(clientEc2,InstancesTagged):
	clientEc2.terminate_instances(DryRun=False,
		InstanceIds=InstancesTagged)

#Creation of a VPC
def createVPC(clientEc2,vpcCidrBlock):
    response = clientEc2.create_vpc(DryRun=False,
            CidrBlock = vpcCidrBlock,
            InstanceTenancy = 'default')

    vpcId = response['Vpc']['VpcId']
    print "VpcId: " + vpcId + " created"

    return vpcId

#get List Instances ID
def getInstancesIdByTag(clientEc2,tag):
	#We get the instances By Tag Value
	response = clientEc2.describe_instances(DryRun=False,
	InstanceIds=[],
	Filters=[{
		'Name': 'tag-value',
		'Values': [tag]
	}])

	reservations = response['Reservations']
#We have on reservation here
	reservation_1 = reservations[0]
#We get the list of instances
	instances = reservation_1['Instances']
	
	instanceList = []

	for instance in instances:
		print instance['InstanceId'] + " is going to be terminated"
		instanceList.append(instance['InstanceId'])

	return instanceList

if __name__ == '__main__':

	#Parsing arguments from CLI
	parser = argparse.ArgumentParser(description='Python program for creating dev environments')
	parser.add_argument('--instances',action="store",type=int ,dest="nbInstances",help='Number of instances you want to create')
	parser.add_argument('--keyName',action="store",type=str, dest="keyName",help="KeyName with which you want to connect")
	parser.add_argument('--sg',action="store",type=str,dest="securityGroup",help="SecurityGroup you want to launch your instances")
	parser.add_argument('--tag',action="store",type=str,dest="tag",help="Tag you want to apply to your resources")
        parser.add_argument('--vpc',action="store",type=str,dest="vpc",help="Specify vpcCidrBlock for your vpc")
        parser.add_argument('--destroy',action="store",type=str,dest="destroyTag",help="Specify the tag for the instances you want to terminate")

	#Storing arguments CLI into variables
	results = parser.parse_args()

	nbInstances = results.nbInstances
	keyName = results.keyName
	securityGroup = results.securityGroup
	tag = results.tag 
	vpcCidr = results.vpc
	destroyTag = results.destroyTag

	#Client connection
	client = boto3.client('ec2')

        if nbInstances is not None:
            #Launching instances
	    print keyName
	    print securityGroup

            instancesList = launchInstances(client,nbInstances,keyName,securityGroup)
            #Tagging instances for later retrieving
            tagResources(client,tag,instancesList)
	    
	if vpcCidr is not None:	
            #Creation of the VPC
	    createVPC(client,vpcCidr)
	
	if destroyTag is not None:
		instancesTagged = getInstancesIdByTag(client,destroyTag)
		terminateInstancesByTag(client,instancesTagged)	
