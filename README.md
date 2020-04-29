# mysql-slow-query-datadog-lambda

AWS Lambda function to relay fingerprint-ed / normalized MySQL Slow Query logs to Datadog.

This function normalizes SQL like below to aggregate metrics on Datadog.

```
SELECT id, name FROM tbl WHERE id = "1000"` => `SELECT id, name FROM tbl WHERE id = ?
SELECT id, name FROM tbl WHERE id IN (10, 20, 30)` => `SELECT id, name FROM tbl WHERE id IN (?+)
```

# How to use
 
1. Generate function.zip file.

```
$ git clone https://github.com/samitani/mysql-slow-query-datadog-lambda.git
$ cd mysql-slow-query-datadog-lambda
$ mkzip.sh
$ ls -l function.zip
-rw-r--r--. 1 root root 17024 Apr 29 22:09 function.zip
```

2. Create Lambda function with generated function.zip

Specify Python3 as Runtime, `main.lambda_handler` as Handler

3. Configure Lambda Environments below

| Key                   | Value         |
|:----------------------|:--------------|
| DD_API_KEY_SECRET_ARN	| AWS Secret Manager ARN of Datadog API KEY.<br>eg) `arn:aws:secretsmanager:ap-northeast-1:XXXXXXXXX:secret:DdApiKeySecret-XXXXXXXX` |
| DD_ENHANCED_METRICS   | false         | 
| DD_SITE               | datadoghq.com |

4. Create Lambda Subscription filter against your Slow Query log CloudWatch Log groups

## Datadog
Generate Metrics with below Grok parser.

```
SlowLogRule ^(\# Time: (%{date("yyMMdd  H:mm:ss"):date}|%{date("yyMMdd HH:mm:ss"):date})\n+)?\# User@Host: %{notSpace: user1}\[%{notSpace: user2}\] @ (%{notSpace: host}| ) *\[%{regex("[0-9.]*"): ip}\]  Id:[\x20\t]+%{number: id}\n+\# Query_time: %{number: query_time} *Lock_time: %{number: lock_time} *Rows_sent: %{number: rows_sent} *Rows_examined: %{number: rows_examined}\n(SET timestamp=%{number: timestamp};\n+)?%{regex("[a-zA-Z].*"):query}.
```
## Note
`enhanced_lambda_metrics.py` and `lambda_function.py` were borrowed from below Datadog repository.

https://github.com/DataDog/datadog-serverless-functions
