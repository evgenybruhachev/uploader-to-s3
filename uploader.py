import boto
import boto.s3
import sys
from boto.s3.key import Key

import os
import os.path

if not sys.argv:
	print 'enter arguments'
        sys.exit()

if len(sys.argv) < 2:
	print 'enter arguments'
        sys.exit()

bucket_prefix = ''

path = sys.argv[1]
deleting_path_part = sys.argv[2]

if not path:
	print 'enter path as first argument'
	sys.exit()

if not deleting_path_part:
	print 'enter removing part of path as second argument'
	sys.exit()

total_count = 0
files = []
for dirpath, dirnames, filenames in os.walk(path):
    for filename in filenames:
	total_count = total_count + 1
	print total_count
        files.append(os.path.join(dirpath, filename))

print len(files)

AWS_ACCESS_KEY_ID = '<insert_access_key_id>'
AWS_SECRET_ACCESS_KEY = '<insert_secret_key>'

bucket_name = '<insert_bucket_name>'
conn = boto.connect_s3(AWS_ACCESS_KEY_ID,
        AWS_SECRET_ACCESS_KEY)


bucket = conn.get_bucket(bucket_name)

total_count = len(files)
counter = 1
for file_for_upload in files:
	print 'Uploading %s to Amazon S3 bucket %s' % \
   	(file_for_upload, bucket_name)
	print '%s of %s' % \
	(counter, total_count)
	def percent_cb(complete, total):
    		sys.stdout.write('.')
    		sys.stdout.flush()
	k = Key(bucket)
	k.key = bucket_prefix + file_for_upload.split(deleting_path_part)[-1]
	k.set_contents_from_filename(file_for_upload,
	    cb=percent_cb, num_cb=10)
	counter = counter + 1