import datetime
import json


#Used to convert datetime to string for json
def dateSerializer(input):
    if isinstance(input, datetime.datetime):
        return input.__str__()