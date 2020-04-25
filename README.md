# Project: lambda-delete-old-keys

A Lambda function and supporting AWS resources to regularly check for and delete all IAM keys which have not been used in than 90 days.

Things that were considered:

1. What users and groups should NOT be touched (administrators, etc in a whitelist).
2. Applications might be running under a key.  At the very least, an mail to engineering.
3. Warning at 80 days that the key will be deleted (to email).
4. Warning at 89 days.
5. Disable key and email.
6. 1 week later delete key and email.
7. Set the execution role of our Lambda (for terraform)
8. Run once a week (this is adjustable)


## Getting Started

1. git clone https://github.com/kwindus/lambda-delete-old-keys.git
2. Run MFA script or one liner (noted here) on your cli to authorize yourself to your AWS account
3. aws sts get-caller-identity to verify your connection
4. If you are using terragrunt, which this example is leveraged on, init yourself with terragrunt init

One liner for MFA:

ENV Vars:

```
unset AWS_SESSION_TOKEN AWS_SECRET_ACCESS_KEY AWS_ACCESS_KEY_ID && export AWS_PROFILE=[profile name]) 
```
then:
```
AWS_MFA_SERIAL=$(aws sts get-caller-identity --query Arn --output text | sed "s/user/mfa/") && eval $(read -p "MFA: " CODE && aws sts get-session-token --serial-number ${AWS_MFA_SERIAL} --token ${CODE} --output=text | awk '{print "export AWS_ACCESS_KEY_ID=" $2 "\n" "export AWS_SECRET_ACCESS_KEY=" $4 "\n" "export AWS_SESSION_TOKEN=" $5}')"
```

Or you can put this included bash script on your lapop.  Store your profiles under ~/.aws/credentials/ or /sessions/ and point the script to that location to read the profile.

Docs:  https://aws.amazon.com/premiumsupport/knowledge-center/authenticate-mfa-cli/
       https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-envvars.html

### Prerequisites

What things you need to install the software and how to install them

```
terraform .12 or above (not tested with newer versions)
terragrunt v0.21.13 or above (not tested with new versions)
AWS Command Line Tools:  https://aws.amazon.com/cli/
Python 3.7 (tested with this version)
pip
Boto3

```

### Installing

Steps:

If you want to deploy the module:
```
cd /path/lambda-key-delete
terragrunt plan -target=module.lambda
terragrunt apply -target=module.lambda
```
Otherwise, you can use the approach straight from the terraform docs:
(https://www.terraform.io/docs/providers/aws/r/lambda_function.html)

### Verify

You can run the pythoon script to see the output:
```
python disable-key.py
```

## Tests

simple tests included in python script

Can also use: Python-lambda: https://github.com/nficano/python-lambda

## Author

* **KGW** 