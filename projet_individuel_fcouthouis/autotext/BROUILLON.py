import dateutil.parser
from datetime import datetime

datestring = '2019-02-12T04:05:55+00:00'
yourdate = dateutil.parser.parse(datestring)
print(yourdate)

dt = datetime.strptime(datestring.replace(":", ""), "%Y-%m-%dT%H%M%S%z")
print(dt)
