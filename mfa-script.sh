#!/usr/bin/env bash

set_aws_profile(){
    unset AWS_ACCESS_KEY_ID
    unset AWS_SECRET_ACCESS_KEY
    unset AWS_SESSION_TOKEN

    export AWS_PROFILE=${1:-prod}
    AWS_MFA_SERIAL=$(aws sts get-caller-identity --query Arn --output text | sed "s/user/mfa/") && eval $(read -p "MFA: " CODE && aws sts get-session-token --serial-number ${AWS_MFA_SERIAL} --token ${CODE} --output=text  | awk '{print "export AWS_ACCESS_KEY_ID=" $2 "\n" "export AWS_EXPIRATION=" $3 "\n" "export AWS_SECRET_ACCESS_KEY=" $4 "\n" "export AWS_SESSION_TOKEN=" $5}')
    export AWS_REGION=$(aws configure get region)
}
cache_aws_profile(){
    unset AWS_EXPIRATION
    export AWS_PROFILE=${1:-prod}
    export AWS_SESSION_FILE_LOCATION="${HOME}/.aws/sessions/${AWS_PROFILE}"
    if [[ ! -f "${AWS_SESSION_FILE_LOCATION}" ]]; then
        mkdir -p $(dirname ${AWS_SESSION_FILE_LOCATION})
        echo > ${AWS_SESSION_FILE_LOCATION}
    fi
    source ${AWS_SESSION_FILE_LOCATION}
    NOW=`date -u "+%Y-%m-%dT%H:%M:%SZ"`
    if [[ ${AWS_EXPIRATION} < $NOW ]]; then
        echo "${AWS_EXPIRATION} < $NOW"
        set_aws_profile ${AWS_PROFILE}
        eval $(aws ecr get-login --no-include-email)
        echo "export AWS_REGION=${AWS_REGION}" > ${AWS_SESSION_FILE_LOCATION}
        echo "export AWS_PROFILE=${AWS_PROFILE}" >> ${AWS_SESSION_FILE_LOCATION}
        echo "export AWS_EXPIRATION=${AWS_EXPIRATION}" >> ${AWS_SESSION_FILE_LOCATION}
        echo "export AWS_ACCESS_KEY_ID=${AWS_ACCESS_KEY_ID}" >> ${AWS_SESSION_FILE_LOCATION}
        echo "export AWS_SECRET_ACCESS_KEY=${AWS_SECRET_ACCESS_KEY}" >> ${AWS_SESSION_FILE_LOCATION}
        echo "export AWS_SESSION_TOKEN=${AWS_SESSION_TOKEN}" >> ${AWS_SESSION_FILE_LOCATION}
    fi
}
cache_aws_profile ${1}