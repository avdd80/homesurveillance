#!/usr/bin/python
# logger.py
# Python script to log messages
# ------------------------------------------------------------------------

#-----------------------------------------#
#-----------------------------------------#
#------- BASH TERMINAL COLOR CODES -------#
# Reset
__Color_Off__='\033[0m'       # Text Reset
#-----------------------------------------#
# Regular Colors
__Black__='\033[0;30m'        # Black
__Red__='\033[0;31m'          # Red
__Green__='\033[0;32m'        # Green
__Yellow__='\033[0;33m'       # Yellow
__Blue__='\033[0;34m'         # Blue
__Purple__='\033[0;35m'       # Purple
__Cyan__='\033[0;36m'         # Cyan
__White__='\033[0;37m'        # White
#-----------------------------------------#
# Bold
__BBlack__='\033[1;30m'       # Black
__BRed__='\033[1;31m'         # Red
__BGreen__='\033[1;32m'       # Green
__BYellow__='\033[1;33m'      # Yellow
__BBlue__='\033[1;34m'        # Blue
__BPurple__='\033[1;35m'      # Purple
__BCyan__='\033[1;36m'        # Cyan
__BWhite__='\033[1;37m'       # White
#-----------------------------------------#
# Underline
__UBlack__='\033[4;30m'       # Black
__URed__='\033[4;31m'         # Red
__UGreen__='\033[4;32m'       # Green
__UYellow__='\033[4;33m'      # Yellow
__UBlue__='\033[4;34m'        # Blue
__UPurple__='\033[4;35m'      # Purple
__UCyan__='\033[4;36m'        # Cyan
__UWhite__='\033[4;37m'       # White
#-----------------------------------------#
# Background
__On_Black__='\033[40m'       # Black
__On_Red__='\033[41m'         # Red
__On_Green__='\033[42m'       # Green
__On_Yellow__='\033[43m'      # Yellow
__On_Blue__='\033[44m'        # Blue
__On_Purple__='\033[45m'      # Purple
__On_Cyan__='\033[46m'        # Cyan
__On_White__='\033[47m'       # White
#-----------------------------------------#
# High Intensity
__IBlack__='\033[0;90m'       # Black
__IRed__='\033[0;91m'         # Red
__IGreen__='\033[0;92m'       # Green
__IYellow__='\033[0;93m'      # Yellow
__IBlue__='\033[0;94m'        # Blue
__IPurple__='\033[0;95m'      # Purple
__ICyan__='\033[0;96m'        # Cyan
__IWhite__='\033[0;97m'       # White
#-----------------------------------------#
# Bold High Intensity
__BIBlack__='\033[1;90m'      # Black
__BIRed__='\033[1;91m'        # Red
__BIGreen__='\033[1;92m'      # Green
__BIYellow__='\033[1;93m'     # Yellow
__BIBlue__='\033[1;94m'       # Blue
__BIPurple__='\033[1;95m'     # Purple
__BICyan__='\033[1;96m'       # Cyan
__BIWhite__='\033[1;97m'      # White
#-----------------------------------------#
# High Intensity backgrounds
__On_IBlack__='\033[0;100m'   # Black
__On_IRed__='\033[0;101m'     # Red
__On_IGreen__='\033[0;102m'   # Green
__On_IYellow__='\033[0;103m'  # Yellow
__On_IBlue__='\033[0;104m'    # Blue
__On_IPurple__='\033[0;105m'  # Purple
__On_ICyan__='\033[0;106m'    # Cyan
__On_IWhite__='\033[0;107m'   # White
#-----------------------------------------#
#-----------------------------------------#

class log_handler(object):

    # Start with log level HIGH
    def __init__(self, enable_logging=True, log_level=7):
        '''
        Initialise class.
        '''
        
        # 1 = Error
        # 3 = High
        # 5 = Med
        # 7 = Low
        # 9 = Notes
        self.__logging_level          = log_level
        self.__LOG_LEVEL_ERROR_MARKER = 1
        self.__LOG_LEVEL_HIGH_MARKER  = 3
        self.__LOG_LEVEL_MED_MARKER   = 5
        self.__LOG_LEVEL_LOW_MARKER   = 7
        self.__LOG_LEVEL_NOTE_MARKER  = 9
        
        print 'log level set to ' + str (self.__logging_level)
        
    def set_log_level (self, log_level):
        self.__logging_level = log_level
    
    def print_error (self, str):
        if self.__LOG_LEVEL_ERROR_MARKER < self.__logging_level:
            print (__BIRed__ + str + __Color_Off__)

    def print_high (self, str):
        if self.__LOG_LEVEL_HIGH_MARKER < self.__logging_level:
            print (__BGreen__ + str + __Color_Off__)

    def print_med (self, str):
        if self.__LOG_LEVEL_MED_MARKER < self.__logging_level:
            print (__Purple__ + str + __Color_Off__)
            
    def print_low (self, str):
        if self.__LOG_LEVEL_LOW_MARKER < self.__logging_level:
            print (str)
            
    def print_notes (self, str):
        if self.__LOG_LEVEL_NOTE_MARKER < self.__logging_level:
            print (__Yellow__ + 'NOTE: ' + str + __Color_Off__)

    @property
    def LOG_LEVEL_ERROR (self):
        return 1
        
    @property
    def LOG_LEVEL_HIGH (self):
        return 3
        
    @property
    def LOG_LEVEL_MED (self):
        return 5
        
    @property
    def LOG_LEVEL_LOW (self):
        return 7
        
    @property
    def LOG_LEVEL_NOTE (self):
        return 9
