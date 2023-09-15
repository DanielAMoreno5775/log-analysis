import pandas as pd



def logToPandaDataFrame(path):
	logData  = open(path, "r")
	splitList = []

	for line in logData:
		if (line != "\n"): #ensures that there aren't any errors from blank lines
			ipAddress = line.split(' ')[0]
			timeStamp = line.split(' ')[3]
			timeStamp = timeStamp[1:]
			utcOffset = line.split(' ')[4]
			utcOffset = utcOffset[:5]
			httpRequest = line.split('"')[1] #gets stuff after first quote
			browserAgent = line.split('"')[5] #gets stuff after fifth quote
			group1 = line.split('"')[2].strip().split(" ") #gets stuff after second quote, strips off spaces before and after text, and splits text into two parts
			httpRESTStatusCode = group1[0]
			bytesTransferred = group1[1]
			
			splitList.append([ipAddress, timeStamp, utcOffset, httpRequest, httpRESTStatusCode, bytesTransferred, browserAgent])
		
	df = pd.DataFrame(splitList, columns=['IP Address', 'Time Stamp', 'UTC Offset', 'HTTP Request', 'HTTP Status Code - REST', 'Bytes Transferred', 'Browser Agent'])
	return df

def bytesTransferred(path):
	log_data  = open(path, "r")
	ipDict = {}

	for line in log_data:
		if (line != "\n"): #ensures that there aren't any errors from blank lines
			responseSize = int(line.split('"')[2].strip().split(' ')[1])
				#breaks 216.218.206.66 - - [30/Sep/2015:00:38:26 -0400] "GET / HTTP/1.1" 502 166 "-" "-" into
				#216.218.206.66 - - [30/Sep/2015:00:38:26 -0400],GET / HTTP/1.1, 502 166 ,-,- and then into
				#502 166 and then into
				#166 and converts it into an integer
			ip = line.split(' ')[0]
			if ip in ipDict:
				ipDict[ip] += responseSize
			else:
				ipDict[ip] = responseSize
	
	print("Number of bytes transferred by each IP Address: %s" % ipDict)
	
def frequencyOfIpAddress(path):
	log_data  = open(path, "r")
	ipDict = {}

	for line in log_data:
		if (line != "\n"): #ensures that there aren't any errors from blank lines
			ip = line.split(' ')[0]
			if ip in ipDict:
				ipDict[ip] += 1
			else:
				ipDict[ip] = 1
	
	print("Number of occurrences of each IP Address: %s" % ipDict)


#gets user input for file name if file is in same folder as program
filePath = input("Enter file name and format: ")
#gets all pertinent log data and formats it as a panda datatable
pandaLogVersion = logToPandaDataFrame(filePath)
print(pandaLogVersion)
#gets number of bytes transferred by each unique IP address
bytesTransferred(filePath)
#gets number of occurrences of each unique IP address
frequencyOfIpAddress(filePath)
