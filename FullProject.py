import boto3
import uuid

def create_bucket_name(bucket_prefix):
    # The generated bucket name must be between 3 and 63 chars long
  
    return ''.join([bucket_prefix, str(uuid.uuid4())])

def create_bucket(bucket_prefix, s3_connection):
    session = boto3.session.Session()
    current_region = session.region_name
    print('current_region',current_region)
    bucket_name = create_bucket_name(bucket_prefix)
    print('bucket_name',bucket_name)
    bucket_response = s3_connection.create_bucket(
        Bucket=bucket_name,
        CreateBucketConfiguration={
        'LocationConstraint': current_region})
    print(bucket_name, current_region)
    return bucket_name, bucket_response

def create_temp_file(size, file_name, file_content):
    random_file_name = ''.join([str(uuid.uuid4().hex[:6]), file_name])
    with open(random_file_name, 'w') as f:
        f.write(str(file_content) * size)
    return random_file_name

def copy_to_bucket(bucket_from_name, bucket_to_name, file_name):
    copy_source = {
        'Bucket': bucket_from_name,
        'Key': file_name
    }
    s3_resource.Object(bucket_to_name, file_name).copy(copy_source) 




s3_resource = boto3.resource('s3')
#print('s3_client',s3_client.meta.client)

first_bucket_name,first_response = create_bucket(bucket_prefix='firstpythonbucket',s3_connection=s3_resource.meta.client)
#secend_bucket_name,secend_response = create_bucket(bucket_prefix='secendpythonbucket',s3_connection=s3_resource)
#print('first_response',first_response)
#print('secend_response',secend_response)

first_bucket_prefix=first_response
first_bucket_name=first_bucket_name

first_file_name = create_temp_file(300, 'firstfile.txt', 'f') 

print('first_bucket_prefix',first_bucket_name)
print('first_file_name',first_file_name)

s3_resource.Object(first_bucket_name, first_file_name).upload_file(
    Filename=first_file_name)

# download file from bucket to tmp local dir
s3_resource.Object(first_bucket_name, first_file_name).download_file(
    f'/tmp/{first_file_name}') # Python 3.6+



#Create secend bucket

second_bucket_name,secend_response = create_bucket(bucket_prefix='secendpythonbucket',s3_connection=s3_resource.meta.client)

#Copy file from first bucket to secend bucket

s3_resource.Object(first_bucket_name, second_bucket_name).copy(first_file_name)

#Delete the file from secend bucket

s3_resource.Object(second_bucket_name, first_file_name).delete()

