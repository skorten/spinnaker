#!/usr/bin/env python

import sys
import re
import pprint
import os

builders = [ 'hvm_builder' ] #might add pv_builds later... not sure.

md_header="""---
layout: toc-page
title: AMI ID table
id: ami_table
lang: en
---

* Table of contents. This line is required to start the list.
{:toc}

# AMI ID Table


| Region         | Name                     | Ubuntu Version | Instance Type | AMI ID       |
|----------------|--------------------------|----------------|---------------|--------------|
"""

def main(argv):
    if len(sys.argv) < 3:
        print "ERROR: You did not give me the output file.\n\tusage: " + sys.argv[0] + " <jenkinsoutputfilelocation> <wheretoputtheartifacts>\n"
        exit(1)

    jenkins_output_file = sys.argv[1]
    artifact_file_location = sys.argv[2]

    if not os.path.isfile(jenkins_output_file):
        print "ERROR: Jenkins output file does not exist (" + jenkins_output_file + ").\n\tusage: " + sys.argv[0] + " <jenkinsoutputfilelocation> <wheretoputtheartifacts>\n"
        exit(1)

    if not os.path.isdir(artifact_file_location):
        print "ERROR: Artifact directory give does not exist (" + artifact_file_location + ").\n\tusage: " + sys.argv[0] + " <jenkinsoutputfilelocation> <wheretoputtheartifacts>\n"
        exit(1)


    pp = pprint.PrettyPrinter(indent=4)
    amis = {}

    artifact_file_md = "ami_table.md"
    artifact_file_json = "ami_table.json"

    fo = open(jenkins_output_file, 'r')

    for line in fo:
        for builder in builders:
            if re.match('^hvm', builder):
                instance_type = 'hvm'
            else:
                instance_type = 'pv'

            if instance_type not in amis:
                amis[instance_type] = {}

            string_to_search_for = ".*" + builder + ': AMIs were created:'

            if re.match(string_to_search_for, line):
                temp_line = re.sub(string_to_search_for, '', line)

                data = temp_line.split("\\n")
                for block in data:
                    if block != '':
                        block = re.sub('\s+', '', block)

                        ( region, ami_id ) = block.split(':')

                        amis[instance_type][region] = ami_id

    fo.close()

    pp.pprint(amis)

    name = 'Spinnaker-Ubuntu-14.04-10'
    ubuntu_version = '14.04 LTS'
    amazon_console_prefix = 'https://console.aws.amazon.com/ec2/home?region='


    md_fo = open(artifact_file_location + '/' + artifact_file_md, 'w+')

    md_fo.write(md_header)

    for instance_type in amis:
        for region in amis[instance_type]:
            ami_id = amis[instance_type][region]

            line_to_write = '|' + region + '|' + name + '|' + ubuntu_version + '|' + instance_type + '|' + '[' + ami_id + '](' + amazon_console_prefix + region + '#launchAmi=' + ami_id + ') |\n'
            md_fo.write(line_to_write)

    md_fo.close()

'''
---
layout: toc-page
title: AMI ID table
id: ami_table
lang: en
---

* Table of contents. This line is required to start the list.
{:toc}

# AMI ID Table


| Region         | Name                     | Ubuntu Version | Instance Type | AMI ID       |
|----------------|--------------------------|----------------|---------------|--------------|
| us-east-1      | Spinnaker-Ubuntu-14.04-10 | 14.04 LTS      | HVM           | [ami-a3afeac9](https://console.aws.amazon.com/ec2/home?region=us-east-1#launchAmi=ami-a3afeac9) |
| us-west-1      | Spinnaker-Ubuntu-14.04-10 | 14.04 LTS      | HVM           | [ami-2796f847](https://console.aws.amazon.com/ec2/home?region=us-west-1#launchAmi=ami-2796f847) |
| us-west-2      | Spinnaker-Ubuntu-14.04-10 | 14.04 LTS      | HVM           | [ami-02766663](https://console.aws.amazon.com/ec2/home?region=us-west-2#launchAmi=ami-02766663) |
| eu-west-1      | Spinnaker-Ubuntu-14.04-10 | 14.04 LTS      | HVM           | [ami-e30dd790](https://console.aws.amazon.com/ec2/home?region=eu-west-1#launchAmi=ami-e30dd790) |
| eu-central-1   | Spinnaker-Ubuntu-14.04-10 | 14.04 LTS      | HVM           | [ami-09203265](https://console.aws.amazon.com/ec2/home?region=eu-central-1#launchAmi=ami-09203265) |
| ap-southeast-1 | Spinnaker-Ubuntu-14.04-10 | 14.04 LTS      | HVM           | [ami-6993520a](https://console.aws.amazon.com/ec2/home?region=ap-southeast-1#launchAmi=ami-6993520a) |
| ap-southeast-2 | Spinnaker-Ubuntu-14.04-10 | 14.04 LTS      | HVM           | [ami-de520bbd](https://console.aws.amazon.com/ec2/home?region=ap-southeast-2#launchAmi=ami-de520bbd) |
| ap-northeast-1 | Spinnaker-Ubuntu-14.04-10 | 14.04 LTS      | HVM           | [ami-9c1033f2](https://console.aws.amazon.com/ec2/home?region=ap-northeast-1#launchAmi=ami-9c1033f2) |
| sa-east-1      | Spinnaker-Ubuntu-14.04-10 | 14.04 LTS      | HVM           | [ami-5d47fd31](https://console.aws.amazon.com/ec2/home?region=sa-east-1#launchAmi=ami-5d47fd31) |
'''


if __name__ == "__main__":
    main(sys.argv)
