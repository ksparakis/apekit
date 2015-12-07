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

import ijson
import random
import requests
import os
from progressbar import ProgressBar
from urllib import urlopen
from backend.model_interface import ModelInterface


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
        self._version           = "v2.0.0"
        self.meta_url           = "https://archive.org/download/playdrone-snapshots/2014-10-31.json"
        self.mi                 = ModelInterface.get_instance()
        self.num_apks           = 0
        self.apks               = list()
        self._pbar              = ProgressBar()
        self._pbar.term_width   = 80
        self._pbar.maxval       = 100  # out of 100%
        self.__progress         = 0
        self.failures           = list()  # holds apk names that failed to download
        self.num_downloads      = 0
       
    
    def __unicode__(self):
        return "Archive Crawler " + self._version
        
    
    def __repr__(self):
        return "Archive Crawler " + self._version

    
    def version(self):
        print "Archive Crawler " + self._version
        

    def sample(self, n):
        '''
            Samples n apks randomly from the archive.org snapshot on 10-31-2014.
            We select a random sampling to get a better representation of the
            market as a whole.
        '''

        del self.apks[:]
        self.num_apks = 0
        
        print "sampling apk repository..."
        self._pbar.start()
        self.__progress = 0
        pstep = 100.0 / n

        # randomly jump through the metadata on archive.org 
        f = urlopen(self.meta_url)
        i = 0
        c = 0
        jump = random.randint(100, 1400)

        for item in ijson.items(f, "item"):         
            i += 1
            if i == jump:
                if 'metadata_url' in item and 'apk_url' in item:
                    self.apks.append(item)
                    self.__progress += pstep
                    self._pbar.update(self.__progress)
                    c += 1
                
                    jump = random.randint(1000, 10000)
                    i = 0
                
                    if c == n:
                        break
        f.close()
        self.num_apks = len(self.apks)
        self._pbar.finish()
        
        for i in range(self.num_apks):
            # cleanup apk metadata 'star_rating' field
            self.apks[i]['star_rating'] = float(self.apks[i]['star_rating'])
            # and generate local filepath based on convention
            self.apks[i]['apk_local'] = "apks/" + self.apks[i]['apk_url'].split('/')[-1]
            
        # save apk metadata to database
        self.mi.add_apps_to_db(self.apks)
    
        print str(self.num_apks) + " apks sampled"
        
        
    def get_permissions(self):
        '''
            Get permissions metadata for sampled apks.
        '''
        
        if self.num_apks <= 0:
            print "no apks sampled"
            return
            
        self._pbar.start()
        self._pbar.maxval = self.num_apks
        self.__progress = 0
        
        for apk in self.apks:
            app_id = apk['app_id']
            meta_url = apk['metadata_url']
            
            meta = requests.get(meta_url).json()
            permissions = meta['details']['permission']
            
            # add permissions to database
            self.mi.add_permissions_for_app(app_id, permissions)
            
            self.__progress += 1
            self._pbar.update(self.__progress)
            
        self._pbar.finish()
        
       
    def download(self, target_dir='apks/'):
        '''
            Downloads the sampled apk files from archive.org.
        '''
        
        if self.num_apks <= 0:
            print "no apks sampled"
            return
        
        if len(target_dir) == 0:
            print "invalid target directory name"
            return
            
        num_apks = self.num_apks
        
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
        print "downloading " + str(num_apks) + " apks from archive.org"
        self._pbar.start()
        self._pbar.maxval = num_apks
        
        # download apks
        self.num_downloads = 0
        del self.failures[:]
        
        for i in range(num_apks):
            try:
                url = self.apks[i]['apk_url']
                self.__download_large_file(url, target_dir)
                self.num_downloads += 1
                
            except (_DownloadError, requests.exceptions.ConnectionError, requests.exceptions.Timeout) as err:
                # note if an apk fails to download, but do not terminate
                self.failures.append(self.apks[i]['app_id'])
                
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
        
            
