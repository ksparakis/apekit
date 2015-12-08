"""
    Top Level Pipeline Module
    EC521 Cyber Security Project
    
    Copyright 2015 Luke Sorenson
    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at
        http://www.apache.org/licenses/LICENSE-2.0
    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.
"""

import fnmatch
import os
import subprocess

from backend.model_interface import ModelInterface
from vulns.vuln_lib_checker import VulnLibChecker
from vulns.keySearch import keySearch
from vulns.httpschecker import httpschecker
from vulns.commentchecker import commentchecker
from charting.charting import chart_vulns

class Pipeline(object):
    """
    Top level module for apekit, which reads the list of downloaded apps,
    decompiles them into java files, reads in the java files and runs the
    lines through a variety of security modules to look for common
    vulnerabilities. These vulnerabilities are then aggregated in a
    database so that we can compute statistics.
    """

    def __init__(self):
        self.counter = 0

    def run(self):
        """
        Runs the pipeline on the apps from the sqlite db.
        """
        mi = ModelInterface.get_instance()
        num_apps = mi.get_num_apps()
        for i in xrange(1, num_apps + 1):
            app = mi.get_app_for_id(i)
            if not app:
                print "Failed to get app for id: " + str(i)
                continue
            dir_name = "decompiled/" + app.app_id
            if not os.path.isdir(dir_name):
                try:
                    subprocess.check_output("python androguard/androdd.py -i " +
                        app.apk_local + " -o " + dir_name + " -l " +
                        app.app_id + "*", shell=True)
                except:
                    print "App " + app.app_id + " could not be decompiled"
                    continue
            files = self.get_java_files_in_dir(dir_name)
            for path_to_file in files:
                self.analyze_file_for_vulns(app, path_to_file)
            print "Finished analyzing app " + app.app_id + "for vulns"
        # Chart the vulnerability results.
        chart_vulns(mi.get_vulnerabilities_and_descriptions(), num_apps)


    @staticmethod
    def analyze_file_for_vulns(app, path_to_file):
        mi = ModelInterface.get_instance()
        vln = VulnLibChecker.get_instance()
        with open(path_to_file) as f:
            line_counter = 1
            for line in f:
                line = line.rstrip()
                # Call the vulnerability analysis modules here.
                if len(line) > 0:
                    # Check for potentially vulnerable library.
                    ids = vln.vulnCheck(line)
                    for vuln_id in ids:
                        mi.add_vulnerability_for_app(
                            app, vuln_id, path_to_file, line_counter, line)
                    # Check for secure keys.
                    is_key = keySearch(line)
                    if is_key[0]:
                        mi.add_vulnerability_for_app(app, 10,
                            path_to_file, line_counter, line)
                    # Check for http instead of https.
                    if httpschecker(line):
                        mi.add_vulnerability_for_app(app, 11,
                            path_to_file, line_counter, line)
                    if commentchecker(line):
                        mi.add_vulnerability_for_app(app, 12,
                            path_to_file, line_counter, line)
                line_counter += 1

    @staticmethod
    def get_java_files_in_dir(directory):
        """
        Returns a list of all java file paths in a directory.
        """
        matches = []
        for root, dirnames, filenames in os.walk(directory):
            for filename in fnmatch.filter(filenames, '*.java'):
                matches.append(os.path.join(root, filename))
        return matches


if __name__ == "__main__":
    pipeline = Pipeline()
    pipeline.run()