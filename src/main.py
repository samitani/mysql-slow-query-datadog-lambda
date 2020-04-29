import lambda_function
import fingerprint

def my_enrich_slow_logs(events):
    for event in events:
        messages = []
        sql = ''
        
        for line in event['message'].split("\n"):
            if line.startswith("#"):
                messages.append(line)
            elif line.startswith("SET timestamp="):
                pass
            elif line.startswith("use "):
                pass
            else:
                sql = sql + line
        
        messages.append(fingerprint.fingerprint(sql))

        event['message'] = "\n".join(messages)

        lambda_function.add_metadata_to_lambda_log(event)
    return events

def lambda_handler(event, context):
    lambda_function.enrich = my_enrich_slow_logs

    return lambda_function.lambda_handler(event, context)


