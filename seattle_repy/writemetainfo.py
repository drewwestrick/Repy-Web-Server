""" 
Author: Justin Cappos

Start Date: August 8, 2008

Description:
Writes the metainfo files used by the software updater.

Usage:  ./writemetainfo.py

"""
# Armon: we use NTP, which uses some repy calls
# This way they have the functions they need
from repyportability import *

import sys
import os  
import os.path

# Used to import repy scripts without polluting the current directory.
import shutil
import tempfile

import repyhelper

repycachedir = tempfile.mkdtemp()

sys.path = [repycachedir] + sys.path
repyhelpercachedir = repyhelper.set_importcachedir(repycachedir)

repyhelper.translate_and_import("rsa.repy")
repyhelper.translate_and_import("signeddata.repy")
repyhelper.translate_and_import("time.repy")

shutil.rmtree(repycachedir)


# Armon: The port that should be used to update our time using NTP
TIME_PORT = 51345

def get_file_hash(filename):
  fileobj = file(filename, 'rb')
  filedata = fileobj.read()
  fileobj.close()

  return sha_hexhash(filedata)


def get_previous_entries():
  if not os.path.exists('metainfo'):
    return {}
    
  returned_dict = {}
  for line in file('metainfo'):
    if line.strip() == '':
      continue
     
    # comment, ignore!
    if line[0] == '#':
      continue

    # signature, ignore
    if line[0] == '!':
      continue

    if len(line.split()) != 3:
      raise Exception, "malformed line: '"+line.strip()+"'"

    # under the file name, store a hash, size tuple
    returned_dict[line.split()[0]] = (line.split()[1], int(line.split()[2]))

  return returned_dict


def create_metainfo_file(privatekeyfilename, publickeyfilename, new=False):
  previous_entries = get_previous_entries()

  outstring = ''
  updatedlist = []

  for filename in os.listdir('.'):
    # ignore pyc files...
    if filename.endswith('.pyc'):
      continue

    # ignore swp files...
    if filename.endswith('.swp'):
      continue
    
    # ignore repy preprocessed files...
    if filename.endswith('_repy.py'):
      continue

    # ignore directories... -Brent
    if os.path.isdir(filename):
      continue

    # ignore the metainfo file
    if filename == 'metainfo':
      continue

    filehash = get_file_hash(filename)
    filesize = os.path.getsize(filename)

    if filename not in previous_entries:
      if not new:
        print "Warning: '"+filename+"' not in previous metainfo file!"

    elif (filehash != previous_entries[filename][0] and filesize == previous_entries[filename][1]) or (filehash == previous_entries[filename][0] and filesize != previous_entries[filename][1]):
      print "Warning, '"+filename+"' has only a hash or file size change but not both (how odd)."

    elif (filehash != previous_entries[filename][0] and filesize != previous_entries[filename][1]):
      # it was updated.   We'll display output to this effect later.
      updatedlist.append(filename)

    outstring = outstring + filename+" "+filehash+" "+str(filesize)+"\n"


  # Okay, great.   We should have it all ready now.   Let's sign our data
  # and report what we're doing
  if not new:
    print "Writing a metafile with updates to:"+ ' '.join(updatedlist)
    
  # Armon: Update our time via NTP
  time_updatetime(TIME_PORT)  

  # timestamp now, expire in 30 days...
  outsigneddata = signeddata_signdata(outstring, rsa_file_to_privatekey(privatekeyfilename), rsa_file_to_publickey(publickeyfilename), time_gettime(), time_gettime()+60*60*24*30)   

  outfo = file("metainfo","w")
  outfo.write(outsigneddata)
  outfo.close()
  
  



def main():
  if len(sys.argv) < 3:
    print "usage: writemetainfo.py privkeyfile publickeyfile [-n]"
    sys.exit(1)

  elif len(sys.argv) > 3 and sys.argv[3] == "-n":
    create_metainfo_file(sys.argv[1], sys.argv[2], True)

  else:
    create_metainfo_file(sys.argv[1], sys.argv[2])
  



if __name__ == '__main__':
  main() 
