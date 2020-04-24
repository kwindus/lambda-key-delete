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
 """
    Return filtered list of users, with whitelisted users excluded.

    >>> filtered_users([{'UserName': 'john'}, {'UserName': 'admin'}], whitelisted={'admin'})
    [{'UserName': 'john'}]

    >>> filtered_users([{'UserName': 'john'}, {'UserName': 'admin'}], whitelisted={})
    [{'UserName': 'john'}, {'UserName': 'admin'}]
    """
    if whitelisted is None:
        whitelisted = whitelisted_users
    return [u for u in all_users if u['UserName'] not in whitelisted]


def contains_whitelisted_group():
    if whitelisted is None:
        whitelisted = whitelisted_groups
    return any(True for g in user_groups if g['GroupName'] in whitelisted)


def decide_actions():
    if 'LastUsedDate' in last_used:
        days_since_last_use = (now - last_used['LastUsedDate'].replace(tzinfo=None)).days
        for days_limit, actions in days_and_actions:
            if days_limit <= days_since_last_use:
                return actions

    return []


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
    def lambda_handler(event, context):
    #print(f"msg: hi")
    client = boto3.client('iam')
    #print(f"msg:  {client}")
    now = datetime.utcnow()


if __name__ == '__main__':
    lambda_handler(None, None)
