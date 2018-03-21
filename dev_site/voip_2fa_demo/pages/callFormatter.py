import shutil, os


def generateCallFile(numList, extension):
    lines = ["Channel: PJSIP/" + str(extension) + "\n",
             "Callerid: 2FA Service\n",
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
        lines[6] = lines[6] + str(formattedNums[i])

    name = ('2fa_' + str(extension) + '.call')
    full_name = (os.path.dirname(os.path.realpath(__file__))) + name
    with open(full_name, 'w') as f:
        f.writelines(lines)

    shutil.move(full_name, "/var/spool/asterisk/outgoing/" + name)
