import shutil
import os


def generateCallFile(numList, extension):
    """
        Takes the string of randomly-generated digits and the user's extension from the log in form
        and generates the .call file that forms the message that asterisk would turn into a voip call
    """
    lines = ["Channel: PJSIP/" + str(extension) + "\n",
             "Callerid: 2FA Service\n",
             "MaxRetries: 1\n",
             "RetryTime: 60\n",
             "WaitTime: 30\n",
             "Application: background\n",
             "Data: silence/1&en/please-enter-the&en/number"
             ]

    formattedNums = []
    # turns the string  of ints into string formatted to match asterisk's stored file that is the audio file of it
    for i in range(6):
        formattedNums.append("&en/digits/" + str(numList[i]))

    # adds the strings created above to lines
    for i in range(6):
        lines[6] = lines[6] + str(formattedNums[i])

    name = ('2fa_' + str(extension) + '.call')
    full_name = (os.path.dirname(os.path.realpath(__file__))) + name
    # creates file in local directory
    with open(full_name, 'w') as f:
        f.writelines(lines)

    # moves the file to /var/spool
    # does not write directly to /var/spool to prevent incomplete messages being read
    shutil.move(full_name, "/var/spool/asterisk/outgoing/" + name)
