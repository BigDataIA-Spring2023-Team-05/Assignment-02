def say_hello():
    return "hello world"

def fetch_url(
    year=int,
    month = int,
    date =int,
    station = str,
    filename = str,
    #date

):

aws_nexrad_url =f'https://noa-nexrad-level2.s3.amazonaws.com/index.html#{year:04}/{month:02}/{date:02}/{station:04}'
return aws_nexrad_url

print(say_hello())
func_op = fetch_url(2022,6,21,'KAMX')
print(func_op)