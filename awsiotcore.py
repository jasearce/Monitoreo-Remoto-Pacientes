import time
import json
import random as rd
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient

def getGeneratedDataFromProteus():
    myData = []
    temperature = rd.randint(24,46)
    heartbeats = rd.randint(50,150)
    myData.extend([temperature,heartbeats])
    return myData;

#Connection to the AWS IoT Core with Root CA certificate and unique device credentials (keys and certificate) previously retrieved

# For certificate based connection
myMQTTClient = AWSIoTMQTTClient("JavierClientID")
# For TLS mutual authentication
myMQTTClient.configureEndpoint("anlboil3rty8h-ats.iot.us-east-1.amazonaws.com", 8883) #Provide your AWS IoT Core endpoint (Example: "abcdef12345-ats.iot.us-east-1.amazonaws.com")

myMQTTClient.configureCredentials("/home/pi/AWSIoT/AmazonRootCA1.pem", "/home/pi/AWSIoT/private.pem.key", "/home/pi/AWSIoT/certificate.pem.crt") #Set path for Root CA and unique device credentials (use the private key and certificate retrieved from the logs in Step 1)

myMQTTClient.configureOfflinePublishQueueing(-1)
myMQTTClient.configureDrainingFrequency(2)
myMQTTClient.configureConnectDisconnectTimeout(10)
myMQTTClient.configureMQTTOperationTimeout(5)

print("Connecting...")
myMQTTClient.connect()
print("Connected!")
#myMQTTClient.subscribe("home/helloworld",1,helloworld)
print("Publishing message to established topic")
counter = 0
while counter < 30:
  dataToSend = getGeneratedDataFromProteus()
  myMQTTClient.publish(topic="device/1/data",QoS=1,payload=json.dumps({'temperature': dataToSend[0], 'heartbeats':dataToSend[1]},indent=4))
  time.sleep(5)
  print("Temperature: %2d and Heartbeats: %2d, published correctly to AWS IoT!" %(dataToSend[0], dataToSend[1]))
  counter+=1
