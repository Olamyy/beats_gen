import stat
import os
import subprocess
from typing import List, Union


class CMDHelper:
    @staticmethod
    def run_cmd_command(args: Union[List, str], return_error_code: bool = False):
        command = subprocess.Popen(args,
                                   stdin=subprocess.PIPE,
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE)
        output, _ = command.communicate()
        decoded_output = output.strip().decode()
        if return_error_code:
            return decoded_output, command.returncode
        return decoded_output

    @staticmethod
    def make_executable(path):
        st = os.stat(path)
        os.chmod(path, st.st_mode | stat.S_IEXEC)
        return True
