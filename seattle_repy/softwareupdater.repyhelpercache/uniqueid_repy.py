# -*- coding: utf-8 -*-
### Automatically generated by repyhelper.py ### /Users/andrewwestrick/Desktop/seattle/seattle_repy/uniqueid.repy

### THIS FILE WILL BE OVERWRITTEN!
### DO NOT MAKE CHANGES HERE, INSTEAD EDIT THE ORIGINAL SOURCE FILE
###
### If changes to the src aren't propagating here, try manually deleting this file. 
### Deleting this file forces regeneration of a repy translation


from repyportability import *
import repyhelper
mycontext = repyhelper.get_shared_context()
callfunc = 'import'
callargs = []

""" 
Author: Justin Cappos

Module: A simple library that provides a unique ID for each call

Start date: November 11th, 2008

This is a really, really simple module, only broken out to avoid duplicating 
functionality.

NOTE: This will give unique ids PER FILE.   If you have multiple python 
modules that include this, they will have the potential to generate the
same ID.

"""

# This is a list to prevent using part of the user's mycontext dict
uniqueid_idlist = [0]
uniqueid_idlock = getlock()

def uniqueid_getid():
  """
   <Purpose>
      Return a unique ID in a threadsafe way

   <Arguments>
      None

   <Exceptions>
      None

   <Side Effects>
      None.

   <Returns>
      The ID (an integer)
  """

  uniqueid_idlock.acquire()

  # I'm using a list because I need a global, but don't want to use the 
  # programmer's dict
  myid = uniqueid_idlist[0]
  uniqueid_idlist[0] = uniqueid_idlist[0] + 1

  uniqueid_idlock.release()

  return myid



### Automatically generated by repyhelper.py ### /Users/andrewwestrick/Desktop/seattle/seattle_repy/uniqueid.repy
