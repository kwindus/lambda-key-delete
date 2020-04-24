import boto3
from datetime import datetime
import logging

logging.basicConfig(format='%(message)s')
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# ordered descending by days, take action on the first that matches
days_and_actions = (
    (96, ['WARN_DELETED', 'DELETE']),
    (90, ['WARN_DISABLED', 'DISABLE']),
    (70, ['WARN']),
)

whitelisted_users = {'Admins'}

whitelisted_groups = {'Admins'}

def filtered_users(all_users, whitelisted=None):
    if whitelisted is None:
        whitelisted = whitelisted_users
    return [u for u in all_users if u['UserName'] not in whitelisted]


def contains_whitelisted_group():


def decide_actions():
    


def take_action(action, access_key):
    print(f"for access_key {access_key} take action {action}")

    if action == 'WARN_DELETED':
        # TODO send email, warning user that access key was deleted
        pass

    elif action == 'DELETE':
        # TODO delete this access key
        pass

    elif action == 'WARN_DISABLED':
        # TODO send email, warning user that access key was deleted
        pass

    elif action == 'DISABLE':
        # TODO disable access key
        pass

    elif action == 'WARN':
        # TODO send email, warning user that access key will be deleted soon
        pass

    else:
        raise ValueError(f"unsupported action: {action}")


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
