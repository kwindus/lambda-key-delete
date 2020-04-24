import stuff

#logging 

# ordered descending by days, take action on the first that matches
days_and_actions = (
)

whitelisted_users = {''}

whitelisted_groups = {''}

def filtered_users():
    
    #Return filtered list of users, with whitelisted users excluded.



def contains_whitelisted_group():


def decide_actions():
    


def take_action(action, access_key):
    print(f"for access_key {access_key} take action {action}")

   ## What actions?  WARN, DISABLE, DELETE


def lambda_handler(event, context):
    #print(f"msg: hi")
    client = boto3.client('iam')
    #print(f"msg:  {client}")
    #get all users
    #see if they are in a whitelist
    #continue if not
    #notify of action on access key id


if __name__ == '__main__':
    #make this testable/runnable without using lambda an just boto3 for now
    lambda_handler(None, None)
