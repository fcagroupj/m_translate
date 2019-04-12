#!/usr/bin/env python
# -*- coding: utf8 -*-
# 			m_translate2.py
# /**
#  * @brief translate all comments in .m files including this foder and subfolers.
#  *
#  * @file od_translate2.py
#  * @author Jeff
#  * @date 2019-4-4
#  */

# ==============================================================================
# -- imports -------------------------------------------------------------------
# ==============================================================================
from __future__ import print_function

import rospy
import os
import os.path
import time
from gotranslate import translate
from random import randint

# ==============================================================================
# -- codes -------------------------------------------------------------------
# ==============================================================================
#
#  translate
#
class runMTranslate(object):
    ## the start entry of this class
    def __init__(self):
        rospy.loginfo("runner.__init__")

        # create a node
        print("welcome to node MTranslate")
        rospy.init_node('m_translate_node',anonymous=True)

        #initialize
	self.statemachine = 100
	rospy.Timer(rospy.Duration(1), self.TimerCb) 

        #running
        rospy.spin()
              
        rospy.on_shutdown(self.exit_hook)
    ## timer 
    def TimerCb(self, data):
	if(self.statemachine <= 0):
	    return
        print("TimerCb")
	self.statemachine = 0
        dirpath = os.getcwd() 
        print("current directory is : " + dirpath)
        ret = 100
        while( ret > 0):
        	ret = self.translateAllFiles(dirpath)
        print("All files are translated.")
        return

    ## find Non Space and seperate
    def findFrontNonSpace(self, line):
	    header = ''
	    tailer = line
	    for ii in range(len(line)):
		if(line[ii] != ' '):
		    header = line[ : ii]
		    tailer = line[ii : ]            
		    return (header, tailer)
	    return (header, tailer)
    ## find Non Space and seperate
    def findRearNonSpace(self, line):
	    header = line
	    tailer = ''
	    llen = len(line)
	    for ii in range(llen):
		if(line[llen-1-ii] != ' '):
		    header = line[ : llen-ii]
		    tailer = line[llen-ii : ]            
		    return (header, tailer)
	    return (header, tailer)
    ## find Non Space and seperate
    def removeReturnLine(self, line):
	    if(line[len(line)-1] == '\n'):
	        return line[: len(line)-1]
	    return line
    ## translate Comments
    def translateComments(self, line):
	    ret = True
	    idx = line.find('% ')
	    if( idx >= 0 ):
		
		header = line[ : idx]
		middle1 = line[idx+2 : ]
		(header2, middle2) = self.findFrontNonSpace(middle1)
		(middle3, tailer3) = self.findRearNonSpace(middle2)

		if(len(middle3) <= 0):
		    return (ret, header + '% ' + header2 + tailer3)
		ret, middle4 =  translate(middle3, to_language="en", from_language="auto") 
		time.sleep(randint(1, 3)/10.0)
		return (ret, header + '% ' + header2 + middle4.encode('utf-8') + tailer3)
	    return (ret, line)

    ## German to English
    def mScriptGerman2Eng(self, infile, outfile):
	    lines_tran = []
	    line_n = 0
	    # translate all
	    with open(infile) as f:
		for line in f:
		    #print (line)
		    if(line_n <= 0):
		        line_n += 1
		        idx = line.find('% Jeff m_translate')  # check the file is translated
		        if(idx == 0):
		            return 10
		    line3 = self.removeReturnLine(line)     # remove the return \n in the tail
		    ret, line2 = self.translateComments(line3)
		    if( ret == False):
		        return 0
		    lines_tran.append(line2)
	    # save all        
	    o_file = open(outfile, "w") 
	    o_file.write( "% Jeff m_translate\n" ) # show the file is translated
	    for line3 in lines_tran:
		o_file.write( line3  + "\n" )   # .encode('utf-8')
	    o_file.close()
	    return 1

    ## translate All Files
    def translateAllFiles(self, i_dirpath):
	    mf_total = 0
	    mf_trans = 0
	    mf_failed = 0
	    for dirpath, dirnames, filenames in os.walk(i_dirpath):
		for filename in [f for f in filenames if f.endswith(".m")]:
		    mf_name = os.path.join(dirpath, filename)
		    print(mf_total, mf_name)

		    ret = self.mScriptGerman2Eng(mf_name, mf_name)
		    if(ret == 10):
		        print("  ignored")
		    elif(ret == 1):
		        print("  translated")
		        mf_trans += 1
		        time.sleep(10 + randint(0, mf_total) )
		        #return (0) # jeff test only
		    else:
		        print("  failed")
		        mf_failed += 1

		    mf_total += 1            

	    print("Total files: %d, Translated files: %d, File failed: %d " % (mf_total, mf_trans, mf_failed) )
	    return (mf_failed)

    ## exit node
    def exit_hook(self):
        print("bye bye, node MTranslate")

#
#  the entry of this application
#
if __name__ == '__main__':
    try:
        runMTranslate()
    except rospy.ROSInterruptException:
        # go away
        pass

## end of file
