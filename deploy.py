import json
import boto
import getpass
import os
import types
import socket
import hashlib
import mime
import logging

from utils import compressString, getURLHeaders, fileSize, retry, getpassword, setpassword, multiMap, internetWorking

#Global path.
PATH = os.getcwd()


class Site(object):

    def __init__(self, path):

        self.path = path

        self.paths = {
            'config': os.path.join(path, 'config.json'),
            'build': os.path.join(path, '.build'),
            'pages': os.path.join(path, 'pages'),
            'templates': os.path.join(path, 'templates'),
            'plugins': os.path.join(path, 'plugins'),
            'static': os.path.join(path, 'static'),
            'script': os.path.join(os.getcwd(), __file__)
        }

        self.config = Config(self.paths['config'])

    def upload(self):
        """
        Upload the site to the server.
        """

        # Make sure we have internet
        if not internetWorking():
            logging.info('There does not seem to be internet here, check your connection')
            return

        logging.debug('Start upload')

        # Get access information from the config or the user
        awsAccessKey = self.config.get('aws-access-key') or \
            raw_input('Amazon access key (http://bit.ly/Agl7A9): ').strip()
        awsSecretKey = getpassword('aws', awsAccessKey) or \
            getpass._raw_input('Amazon secret access key (will be saved in keychain): ').strip()

        # Try to fetch the buckets with the given credentials
        connection = boto.connect_s3(awsAccessKey.strip(), awsSecretKey.strip())

        logging.debug('Start get_all_buckets')
        # Exit if the information was not correct
        try:
            buckets = connection.get_all_buckets()
        except:
            logging.info('Invalid login credentials, please try again...')
            return
        logging.debug('end get_all_buckets')

        # If it was correct, save it for the future
        self.config.set('aws-access-key', awsAccessKey)
        self.config.write()

        setpassword('aws', awsAccessKey, awsSecretKey)

        awsBucketName = self.config.get('aws-bucket-name') or \
            raw_input('S3 bucket name (www.yoursite.com): ').strip().lower()

        if awsBucketName not in [b.name for b in buckets]:
            if raw_input('Bucket does not exist, create it? (y/n): ') == 'y':

                logging.debug('Start create_bucket')
                try:
                    awsBucket = connection.create_bucket(awsBucketName, policy='public-read')
                except boto.exception.S3CreateError, e:
                    logging.info('Bucket with name %s already is used by someone else, please try again with another name' % awsBucketName)
                    return
                logging.debug('end create_bucket')

                # Configure S3 to use the index.html and error.html files for indexes and 404/500s.
                awsBucket.configure_website('index.html', 'error.html')

                self.config.set('aws-bucket-website', awsBucket.get_website_endpoint())
                self.config.set('aws-bucket-name', awsBucketName)
                self.config.write()

                logging.info('Bucket %s was selected with website endpoint %s' % (self.config.get('aws-bucket-name'), self.config.get('aws-bucket-website')))
                logging.info('You can learn more about s3 (like pointing to your own domain) here: https://github.com/koenbok/Cactus')


            else: return
        else:

            # Grab a reference to the existing bucket
            for b in buckets:
                if b.name == awsBucketName:
                    awsBucket = b

        self.config.set('aws-bucket-website', awsBucket.get_website_endpoint())
        self.config.write()

        logging.info('Uploading site to bucket %s' % awsBucketName)

        # Upload all files concurrently in a thread pool
        totalFiles = multiMap(lambda p: p.upload(awsBucket), self.files())
        changedFiles = [r for r in totalFiles if r['changed'] == True]


        # Display done message and some statistics
        logging.info('\nDone\n')

        logging.info('%s total files with a size of %s' % \
            (len(totalFiles), fileSize(sum([r['size'] for r in totalFiles]))))
        logging.info('%s changed files with a size of %s' % \
            (len(changedFiles), fileSize(sum([r['size'] for r in changedFiles]))))

        logging.info('\nhttp://%s\n' % self.config.get('aws-bucket-website'))


    def files(self):
        """
        List of build files.
        """
        return [File(self, p) for p in fileList(self.paths['build'], relative=True)]




#Taken from https://github.com/koenbok/Cactus/blob/master/cactus/site.py
#Used to hold the config file for AWS.
class Config(object):

    def __init__(self, path):
        self.path = path
        self.load()

    def get(self, key):
        return self._data.get(key, None)

    def set(self, key, value):
        self._data[key] = value

    def load(self):
        try:
            self._data = json.load(open(self.path, 'r'))
        except:
            self._data = {}

    def write(self):
        json.dump(self._data, open(self.path, 'w'), sort_keys=True, indent=4)


class File(object):

    CACHE_EXPIRATION = 60 * 60 * 24 * 7 # One week
    COMPRESS_TYPES = ['html', 'css', 'js', 'txt', 'xml']
    COMPRESS_MIN_SIZE = 1024 # 1kb
    PROGRESS_MIN_SIZE = (1024 * 1024) / 2 # 521 kb

    def __init__(self, site, path):
        print site
        print path
        self.site = site
        self.path = path

        self.paths = {
            'full': os.path.join(PATH, '.build', self.path)
        }

    def data(self):
        if not hasattr(self, '_data'):
            f = open(self.paths['full'], 'r')
            self._data = f.read()
            f.close()
        return self._data

    def payload(self):
        """
        The representation of the data that should be uploaded to the
        server. This might be compressed based on the content type and size.
        """
        if not hasattr(self, '_payload'):
            if self.shouldCompress():
                self._payload = compressString(self.data())
            else:
                self._payload = self.data()

        return self._payload
        return self.data()

    def checksum(self):
        """
        An amazon compatible md5 of the payload data.
        """
        return hashlib.md5(self.payload()).hexdigest()

    def remoteChecksum(self):
        return getURLHeaders(self.remoteURL()).get('etag', '').strip('"')

    def remoteURL(self):
        return 'http://%s/%s' % (self.site.config.get('aws-bucket-website'), self.path)

    def extension(self):
        return os.path.splitext(self.path)[1].strip('.').lower()

    def shouldCompress(self):

        if not self.extension() in self.COMPRESS_TYPES:
            return False

        if len(self.data()) < self.COMPRESS_MIN_SIZE:
            return False

        return True

    @retry(socket.error, tries=5, delay=3, backoff=2)
    def upload(self, bucket):

        self.lastUpload = 0
        headers = {'Cache-Control': 'max-age=%s' % self.CACHE_EXPIRATION}

        if self.shouldCompress():
            headers['Content-Encoding'] = 'gzip'

        changed = self.checksum() != self.remoteChecksum()

        if changed:

            # Show progress if the file size is big
            progressCallback = None
            progressCallbackCount = int(len(self.payload()) / (1024 * 1024))

            if len(self.payload()) > self.PROGRESS_MIN_SIZE:
                def progressCallback(current, total):
                    if current > self.lastUpload:
                        uploadPercentage = (float(current) / float(total)) * 100
                        print('+ %s upload progress %.1f%%' % (self.path, uploadPercentage))
                        self.lastUpload = current

            # Create a new key from the file path and guess the mime type
            key = bucket.new_key(self.path)
            mimeType = mime.guess(self.path)

            if mimeType:
                key.content_type = mimeType

            # Upload the data
            key.set_contents_from_string(self.payload(), headers,
                policy='public-read',
                cb=progressCallback,
                num_cb=progressCallbackCount)

        op1 = '+' if changed else '-'
        op2 = ' (%s compressed)' % (fileSize(len(self.payload()))) if self.shouldCompress() else ''

        print('%s %s - %s%s' % (op1, self.path, fileSize(len(self.data())), op2))

        return {'changed': changed, 'size': len(self.payload())}


def fileList(paths, relative=False, folders=False):
    """
    Generate a recursive list of files from a given path.
    """

    if not type(paths) == types.ListType:
        paths = [paths]

    files = []

    for path in paths:
        for fileName in os.listdir(path):

            if fileName.startswith('.'):
                continue

            filePath = os.path.join(path, fileName)

            if os.path.isdir(filePath):
                if folders:
                    files.append(filePath)
                files += fileList(filePath)
            else:
                files.append(filePath)

        if relative:
            files = map(lambda x: x[len(path) + 1:], files)

    return files


def files(site):
        """
        List of build files.
        """
        build_path = os.path.join(PATH, '.build')
        print fileList(build_path, relative=True)
        return [File(site, p) for p in fileList(build_path, relative=True)]
