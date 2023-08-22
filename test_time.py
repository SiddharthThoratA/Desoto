import pytz
from datetime import datetime,timedelta
#import pywhatkit

import pymsteams

def send_msg_teams(script_name):
    message = "Alert! {} got falied, Kindly look into".format(script_name)
    myTeamsMessage = pymsteams.connectorcard("https://o365spi.webhook.office.com/webhookb2/a85a3881-3682-4c1d-bec8-30dd88a8edca@bdeeee28-22ab-472f-8510-87812e5557e1/IncomingWebhook/45f394a4272849bab5cad5ce52fa8a4a/329a3b08-1316-452c-a496-6ab47e68127d")
    myTeamsMessage.text(message)
    myTeamsMessage.send()



#pst = pytz.timezone('America/Los_Angeles')
#p_time = datetime.now(pst)
#pst_time = p_time.strftime('%Y-%m-%d')

#print("current PST date :",pst_time)
#print('Current Date Time in PST =', datetime.now(pst))




