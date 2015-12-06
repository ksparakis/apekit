'''
    PlayDrone Repository Crawler
    EC521 Cyber Security Project
    
    Copyright 2015 Carlton Duffett

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

        http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.
'''

import requests
import grequests
import re
import os
import math
from progressbar import ProgressBar


class _DownloadError(Exception):
    '''
        Custom exception for failed apk downloads.
    '''
    def __init__(self, msg):
        self.msg = msg
    
    def __str__(self):
        return self.msg
            

class ArchiveCrawler(object):
    '''
        Utility that crawls all of the apks stored on archive.org and 
        downloads the first n apk files found. This utility leverages
        the archive.org advanced search API for obtaining the apk metadata. 
        The downloads are obtained directly from the archive.org download API.
    ''' 
    
    def __init__(self):
        self._version       = "v1.0.0"
        
        self.archive_url    = "https://archive.org/details/playdrone-apks/"
        self.meta_url       = "https://www.archive.org/advancedsearch.php"
        self.download_url   = "http://archive.org/download/"
        
        self.num_apks       = 0
        self.num_repos      = 0
        self.repos          = list()
        self.apks           = list()
        self.MAX_REPOS      = 1000  # there are less than 1000 known apk repositories
        
        self._pbar              = ProgressBar()
        self._pbar.term_width   = 80
        self._pbar.maxval       = 100  # out of 100%
        self.__progress         = 0
        
        self.failures       = list()  # holds apk names that failed to download
        self.num_downloads  = 0
       
    
    def __unicode__(self):
        return "Archive Crawler " + self._version
        
    
    def __repr__(self):
        return "Archive Crawler " + self._version

    
    def version(self):
        print "Archive Crawler " + self._version
        

    def index_archive(self):
        '''
            Indexes archive.org to find all available apk names and repositories.
        '''

        # clear if previously initialized
        del self.repos[:]
        self.num_repos = 0
        
        del self.apks[:]
        self.num_apks = 0
        
        print "indexing apk repositories ..."
        self._pbar.start()
        
        # get all identifiers (repository of apk files)
        params = {
            'q':'(playdrone-apk) AND oai_updatedate:2014-08-07',
            'fl[]':'identifier',
            'rows': self.MAX_REPOS,
            'output': 'json',
        }
        r = requests.get(self.meta_url, params=params)
        self.__progress = 50
        self._pbar.update(self.__progress)
        
        for item in r.json()["response"]["docs"]:
            self.repos.append(self.download_url + item["identifier"] + "/")
        
        self.num_repos = len(self.repos)
        self._pbar.finish()
        print str(self.num_repos) + " repositories found"
        
        # asynchronously scan for total number of apks available
        print "indexing apks ..."
        self._pbar.start()
        self.__progress = 0
        
        reqs = list()
        
        for u in self.repos:
            rs = grequests.get(u, hooks=dict(response=self.__process_meta))
            reqs.append(rs)
        
        grequests.map(reqs)
        self._pbar.finish()
        print str(self.num_apks) + " apks found"


    def __process_meta(self, r, **kwargs):
        '''
            Callback for each asynchronous metadata request.
        '''
        
        # parse html index file links for apk names
        matches = re.findall(r'(>[\w\.\-]+apk)',r.text)[2:]  # first two items are garbage
        r.close()
        repo = r.url.split('/')[-2]  # recover repository name from request
        
        # store parsed apk names
        self.num_apks += len(matches)
        for match in matches:
            self.apks.append(repo + '/' + match[1:])
        
        if self.__progress < 99:  # hang at 99% until complete
            self.__progress += 0.5
            self._pbar.update(self.__progress)
            
            
    def load(self, filename='apks.txt'):
        '''
            Loads apk metadata previously saved to specified <filename>.
            If none specified, attempts to load the metadata from apks.txt.
        '''
        
        if len(filename) == 0:
            print "invalid file name"
            return
            
        if not os.path.isfile(filename):
            print "specified file does not exist: " + filename
            return
            
        else:
            
            # metadata file found
            print "loading metadata from " + filename + " ..."
            
            # clear previous metadata
            del self.repos[:]
            self.num_repos = 0
            
            del self.apks[:]
            self.num_apks = 0
            
            f = open(filename, 'r')
            lines = f.readlines()
            
            try:
                self.num_apks = int(lines[0])
            except ValueError as err:
                print "invalid file format"
                return
            
            self._pbar.start()
            self._pbar.update(34)  # arbitrary, for effect
            
            # process metadata from file  
            for line in lines[1:]:
                self.apks.append(line[:-1])
                    
                repo = line.split('/')[0]
                if not repo in self.repos:
                    self.repos.append(repo)
                    
            f.close()
            self.num_apks = len(self.apks)  
            self.num_repos = len(self.repos)
            self._pbar.finish()
            
            print "loaded " + str(self.num_repos) + " repositories and " + str(self.num_apks) + " apk names"
                
    
    def save(self, filename='apks.txt'):
        '''
            Writes the collected apk names to the specified <filename>.
            If none specified, writes the results to "apks.txt".
        '''

        # check for valid filename
        if len(filename) == 0:
            print "invalid file name"
            return
        
        # check if the <filename> file already exists. If so, add
        # an integer to its name and try again.
        # e.g. apks.txt -> apks1.txt -> apks2.txt, etc.
        fno = 1
        while os.path.isfile(filename):
            
            _old = filename
            
            if not filename.find('.') == -1:    
                parts = filename.split('.')
                
                if fno == 1:
                    parts[-2] += str(fno)
                else:
                    parts[-2] = parts[-2][:-1] + str(fno)
                
                filename = '.'.join(parts)
                fno += 1
            
            else:
                # filename has no extension
                if fno == 1:
                    filename += str(fno)
                else:
                    filename = filename[:-1] + str(fno)
                    
                fno += 1
                
            print _old + " already exists, trying " + filename
    
        f = open(filename, 'w')
        print "writing apk metadata to " + filename + " ..."
        
        # init progress bar
        self._pbar.start()
        
        # write number of apk names to first line of file
        f.write(str(self.num_apks) + '\n')
        
        # write apk names and update progress
        f.write('\n'.join(self.apks))
        self.__progress = 60  # arbitrary, for effect
        self._pbar.update(self.__progress)
        f.write('\n')
        f.close()
        self._pbar.finish()

        print str(self.num_apks) + " apk names written to " + filename

       
    def download(self, num_apks, target_dir='apks/'):
        '''
            Downloads the specified number of apk files from archive.org. If no
            target directory is specified, the apks are written locally to apks/.
            To download EVERY apk file, pass 'all' instead of an integer, e.g.:
            
            c.download('all')
        '''
        
        if len(target_dir) == 0:
            print "invalid target directory name"
            return

        if str(num_apks).lower() == 'all':
            num_apks = self.num_apks
        
        else:
            try:
                num_apks = int(num_apks)
            
            except ValueError as err:
                print "invalid number of apks specified"
                return
                
            if num_apks < 1:
                print "invalid number of apks specified"
                return
                
        # check that apk metadata is already loaded
        if not self.apks:
            
            # attempt to read metadata from file
            print "no metadata loaded, looking for metadata file ..."
            self.load()
            
            if not self.apks:
                print "no metadata found, use index_archive() to generate new metadata"
                return      
        
        if num_apks > self.num_apks:
            print "exceeded number of available apks"
            return
        
        # check to see if the <target_dir> directory currently exists
        # if so, append an integer to the directory name and try again
        # e.g. apks/ -> apks1/ -> apks2/ etc.
        if not target_dir[-1] == '/':
            target_dir += '/'
            
        dno = 1
        while os.path.isdir(target_dir):
            
            parts = target_dir.rsplit('/', 1)
            
            if dno == 1:
                parts[-2] += str(dno)
            else:
                parts[-2] = parts[-2][:-1] + str(dno)

            target_dir = '/'.join(parts)
            dno += 1
            
        # create new directory for apks
        os.mkdir(target_dir)
                
        # init progress bar
        print "downloading " + str(num_apks) + " apks from " + self.download_url
        self._pbar.start()
        self._pbar.maxval = num_apks
        
        # download apks
        self.num_downloads = 0
        del self.failures[:]
        
        for i in range(num_apks):
            try:
                url = self.download_url + self.apks[i]
                self.__download_large_file(url, target_dir)
                self.num_downloads += 1
                
            except (_DownloadError, requests.exceptions.ConnectionError, requests.exceptions.Timeout) as err:
                # note if an apk fails to download, but do not terminate
                self.failures.append(apk_names[i])
                
            except KeyboardInterrupt as err:
                self._pbar.finish()
                self._pbar.maxval = 100
                print "download interrupted, " + str(self.num_downloads) + " apks downloaded"
                return
                
            self._pbar.update(i + 1)
        
        self._pbar.finish()
        self._pbar.maxval = 100  # restore default
        self.__progress = 0
        
        print "successfully downloaded " + str(num_apks - len(self.failures)) + " apks to " + target_dir
        
        if self.failures:
            print "the following items failed to download:"
            for fail in self.failures:
                print fail


    def __download_large_file(self, url, target_dir):
        '''
            mutipart download of large apk files
        '''
        
        try:
            local_filename = target_dir + url.split('/')[-1]
            r = requests.get(url, stream=True)
            
            if r.status_code == 404:
                raise _DownloadError(local_filename)
            
            with open(local_filename, 'wb') as f:
                for chunk in r.iter_content(chunk_size=1024):
                    if chunk: # filter out keep-alive new chunks
                        f.write(chunk)     
                f.close()
            
            return local_filename
            
        except KeyboardInterrupt as err:
            # cleanup
            if f:
                f.close()
                os.remove(local_filename)
                
            raise KeyboardInterrupt
            
