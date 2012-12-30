import os
import sys
import shutil
import logging
import subprocess
import webbrowser
import getpass
import imp
import base64
import traceback
import socket
import tempfile

import boto

from deploy import Config
from utils import *
from deploy import File

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

