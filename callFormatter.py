#!/usr/bin/python3

testList=[1,2,3,4,5,6]

def generateCallFile(numList, extension):
    lines = [ "Channel: PJSIP/" + str(extension) + "\n",
        "MaxRetries: 1\n",
        "RetryTime: 60\n",
        "WaitTime: 30\n",
        "Application: background\n",
        "Data: silence/1&en/please-enter-the&en/number"
    ]

    formattedNums = []
    for i in range(6):
        formattedNums.append("&en/digits/" + str(numList[i]))
        
    for i in range(6):
        lines[5] = lines[5] + str(formattedNums[i])

    name = ('2fa_' + str(extension) + '.call') 
    with open(name, 'w') as f:
        f.writelines(lines)
    
    
if __name__ == "__main__":
    generateCallFile(testList, 42)
