AWS Wizard

More information available on https://aws-wizard.com 



Done:
domain bucket creation
cert request
cloudfront creation
routing to cloudfront
route to s3 before routing to cloudfront
- router config (print records)
- router interactive config (interactive check via "host -t ns DOMAIN") //whois updates faster than host-t-ns

Todo:
- provide feedback on records set propagation status (route53.change-resource-record-sets.output ChangeInfo.Status?)
- cert interactive config (wait for validation)
- multiregional setup support
- handle domains purchased on amazon: add ns records via script?



python3 setup.py sdist