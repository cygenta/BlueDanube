import dns.name
import dns.message
import dns.query
import dns.flags
import argparse
import concurrent.futures
import random

'''
██████╗ ██╗     ██╗   ██╗███████╗██████╗  █████╗ ███╗   ██╗██╗   ██╗██████╗ ███████╗
██╔══██╗██║     ██║   ██║██╔════╝██╔══██╗██╔══██╗████╗  ██║██║   ██║██╔══██╗██╔════╝
██████╔╝██║     ██║   ██║█████╗  ██║  ██║███████║██╔██╗ ██║██║   ██║██████╔╝█████╗  
██╔══██╗██║     ██║   ██║██╔══╝  ██║  ██║██╔══██║██║╚██╗██║██║   ██║██╔══██╗██╔══╝  
██████╔╝███████╗╚██████╔╝███████╗██████╔╝██║  ██║██║ ╚████║╚██████╔╝██████╔╝███████╗
╚═════╝ ╚══════╝ ╚═════╝ ╚══════╝╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═══╝ ╚═════╝ ╚═════╝ ╚══════╝
                                                                                    
Name:  BlueDanube
Author: Freakyclown @ Cygenta Ltd Twitter:@CygentaHQ
Status: External Tool
Release Date: April 2020
Origin: Named after the British Nuclear weapon
Description: Tool for performming DNS lookups for tens of millions of records
Limitations: Will easily get you blocked by DNS servers for being too fast
Provided sync version for preventing blocking - super slow though for lots of files
Usage: Python3 bluedanube.py -iL {file of urls} > output.file
Arguments: Takes in file of URLs, one per line using -iL
Requirements: Python3

Other Notes: Replace nameservers with servers of your choice

                                                                                          
'''



# Do argument parsing stuff

parser = argparse.ArgumentParser()
parser.add_argument('-iL', help=' Input List of domains, one domain per line', required=True)
args = parser.parse_args()

# prepare lists etc
inputlist = args.__dict__['iL']
doms = []

# open up the input list and strip off the newline and place in the doms list
with open(inputlist) as fp:
    
    line = fp.readline()
    cnt = 1
    while line:
        doms.append(line.rstrip())
        line = fp.readline()
        cnt += 1

# here are our name servers - we pick from this list at random to avoid blocking.
dnsservers = ['8.8.8.8','208.67.222.222','8.8.4.4','9.9.9.9']


#function for scraping all the things

def scrape(dom):
    try:
        print("Scraping records for:"+dom)
        ADDITIONAL_RDCLASS = 65535
        name_server = random.choice(dnsservers)
        domain = dns.name.from_text(dom.rstrip())
        if not domain.is_absolute():
            domain = domain.concatenate(dns.name.root)

        request = dns.message.make_query(domain, dns.rdatatype.ANY)
        request.flags |= dns.flags.AD
        request.find_rrset(request.additional, dns.name.root, ADDITIONAL_RDCLASS,
                dns.rdatatype.OPT, create=True, force_unique=True)
        response = dns.query.udp(request, name_server, timeout=1)
    
        print(response)
        print("Finished Scraping")
    except:
        pass

# thread all the things!
with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
	executor.map(scrape, doms)

