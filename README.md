## Bare Bones Backup (code base)
### About:  
Bare Bones Backup (B3) is a very simple file backup utility.   
The files in this code base are the 'back end' for a GUI version of the same.  
The idea is to experiment with several Python GUI App builders using a common code base.  
But the code base has to actually do something so it can be tested across devices.  
  
### Basic Features:
B3 is an app that mirrors files in a directory to another location.  
B3 can compare the files in two directories for differences.  
B3 can exclude directories by name.  
B3 can exclude files by name.  
With the excludes, wild cards are implied.  
B3 may or may not delete orphan files in the target directory.  
B3 can have multiple profiles.  
B3 can be set to automatically mirror at a given time.  
B3 is i18n compliant.  