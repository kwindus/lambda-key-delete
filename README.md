# Project: lambda-key-delete

A Lambda function and supporting AWS resources to regularly check for and delete all IAM keys which have not been used in than 90 days.

Things that were considered:

1. What users and groups should NOT be touched (administrators, etc in a whitelist).
2. Applications might be running under a key.  At the very least, a notification.
3. Warning at xx days that the key will be deleted (to email).
4. Warning at xx days.
5. At xx days, disable/delete key and email.

Getting started:
1. git clone https://github.com/kwindus/lambda-delete-old-keys.git
2. Run MFA script or one liner (noted here) on your cli to authorize yourself to your AWS account
3. aws sts get-caller-identity to verify your connection
4. If you are using terragrunt, which this example is leveraged on, init yourself with terragrunt init