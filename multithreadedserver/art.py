sword = """
                           ___
                          ( ((
                           ) ))
  .::.                    / /(
 'M .-;-.-.-.-.-.-.-.-.-/| ((::::::::::::::::::::::::::::::::::::::::::::::.._
(J ( ( ( ( ( ( ( ( ( ( ( |  ))   -====================================-      _.>
 `P `-;-`-`-`-`-`-`-`-`-\| ((::::::::::::::::::::::::::::::::::::::::::::::''
  `::'                    \ \(
                           ) ))
                          (_((
"""

help_menu = """
"help menu"               Print out this menu
"background session"     Check all the sessions
"upload /path/to/file"    Upload a file to remote machime
"download /path/to/file"  Download a file from the remote machine
"screenshot"              Click a screenshot from the remote machine
"pty [port]"              Spawn a shell session from the remote machine to self on defined port
"ls"                      List all files
"cat [file name]"         Cat out contents of the file
"cd [dir/name]"           Change directory
"!DISCONNECT"             Disconnect the current session
"""

colors = {
    'HEADER': '\033[95m',
    'OKBLUE': '\033[94m',
    'OKGREEN': '\033[92m',
    'WARNING': '\033[93m',
    'FAIL': '\033[91m',
    'BOLD': '\033[1m',
    'UNDERLINE': '033[4m',
    'END': '\033[0m',
    'NC': '\x1b[0m'
}