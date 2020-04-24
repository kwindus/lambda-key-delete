import boto3
from datetime import datetime
import logging

logging.basicConfig(format='%(message)s')
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# ordered descending by days, take action on the first that matches
# for safety I have not made calls to the API to actually disable or delete
days_and_actions = (
    (90, ['WARN_DELETED', 'DELETE']),
    (89, ['WARN_DISABLED', 'DISABLE']),
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


def contains_whitelisted_group(user_groups, whitelisted=None):
    """
    Return True if any of the user groups is a whitelisted group.

    >>> contains_whitelisted_group([{'GroupName': 'john'}, {'GroupName': 'admin'}], whitelisted={'admin'})
    True

    >>> contains_whitelisted_group([{'GroupName': 'john'}, {'GroupName': 'admin'}], whitelisted={})
    False

    """
    if whitelisted is None:
        whitelisted = whitelisted_groups
    return any(True for g in user_groups if g['GroupName'] in whitelisted)


def decide_actions(last_used, now):
    """
    Decide what to do with the access key, depending on the days elapsed since last access.

    >>> decide_actions({}, datetime.now())
    []

    >>> decide_actions({'LastUsedDate': datetime.now()}, datetime.now())
    []

    >>> from datetime import timedelta
    >>> decide_actions({'LastUsedDate': datetime.now() - timedelta(days=100)}, datetime.now())
    ['WARN_DELETED', 'DELETE']

    >>> decide_actions({'LastUsedDate': datetime.now() - timedelta(days=90)}, datetime.now())
    ['WARN_DISABLED', 'DISABLE']

    >>> decide_actions({'LastUsedDate': datetime.now() - timedelta(days=85)}, datetime.now())
    ['WARN']

    >>> decide_actions({'LastUsedDate': datetime.now() - timedelta(days=55)}, datetime.now())
    []

    """
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
    client = boto3.client('iam')
    now = datetime.utcnow()

    all_users = client.list_users()['Users']
    users = filtered_users(all_users)

    for user in users:
        username = user['UserName']
        logger.info(username)

        user_groups = client.list_groups_for_user(UserName=username)['Groups']
        if contains_whitelisted_group(user_groups):
            logger.info(whitelisted_groups)
            continue

        access_keys = client.list_access_keys(UserName=username)['AccessKeyMetadata']
        for access_key in access_keys:
            access_key_id = access_key['AccessKeyId']
            print("msg: " + access_key_id)

            last_used = client.get_access_key_last_used(AccessKeyId=access_key_id)['AccessKeyLastUsed']
            for action in decide_actions(last_used, now):
                take_action(action, access_key)

if __name__ == '__main__':
    lambda_handler(None, None)
