from netmiko.ssh_connection import SSHConnection
import re

class CiscoXrSSH(SSHConnection):

    def send_config_set(self, config_commands=None, commit=False):
        '''
        Send in a set of configuration commands as a list

        The commands will be executed one after the other

        Automatically exits/enters configuration mode.

        Optionally perform a commit action
        '''

        if config_commands is None:
            return ''

        if type(config_commands) != type([]):
            raise ValueError("Invalid argument passed into send_config_set")

        # Enter config mode (if necessary)
        output = self.config_mode()

        for a_command in config_commands:
            output += self.send_command(a_command, strip_prompt=False, strip_command=False)

        if commit:
            output += self.commit()

        output += self.exit_config_mode()

        return output


    def commit(self):
        '''
        Commit the entered configuration. Raise an error
        and return the failure if the commit fails.

        IOS-XR commit command must be in config mode
        '''

        # Enter config mode (if necessary)
        output = self.config_mode()

        output += self.send_command('commit', 
                    strip_prompt=False, strip_command=False)

        if "Failed to commit" in output:
            fail_msg = self.send_command('show configuration failed',
                                     strip_prompt=False, strip_command=False)

            raise ValueError('Commit failed with the following errors:\n\n \
                        {fail_msg}'.format(fail_msg=fail_msg))

        output += self.exit_config_mode()
        return output


    def normalize_linefeeds(self, a_string):
        '''
        Convert '\r\n','\r\r\n', '\n\r', or '\r' to '\n
        '''

        newline = re.compile(r'(\r\r\n|\r\n|\n\r|\r)')

        return newline.sub('\n', a_string)


