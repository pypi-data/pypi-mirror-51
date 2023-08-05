# -*- coding: utf-8 -*-

# This code is part of Qiskit.
#
# (C) Copyright IBM 2018, 2019.
#
# This code is licensed under the Apache License, Version 2.0. You may
# obtain a copy of this license in the LICENSE.txt file in the root directory
# of this source tree or at http://www.apache.org/licenses/LICENSE-2.0.
#
# Any modifications or derivative works of this code must retain this
# copyright notice, and modified files need to carry a notice indicating
# that they have been altered from the originals.

"""Chemistry User Interface run experiment thread"""

import threading
import tempfile
import sys
import logging
import io
import platform
import os
import subprocess
import traceback
import psutil
from qiskit_aqua_interfaces.user_interface import GUIProvider

logger = logging.getLogger(__name__)


def exception_to_string(excp):
    """ exception string formatter """
    stack = traceback.extract_stack()[:-3] + traceback.extract_tb(excp.__traceback__)
    pretty = traceback.format_list(stack)
    return ''.join(pretty) + '\n  {} {}'.format(excp.__class__, excp)


class ChemistryThread(threading.Thread):
    """ Chemistry Thread """
    def __init__(self, model, output, queue, filename):
        super(ChemistryThread, self).__init__(name='Chemistry run thread')
        self.model = model
        self._output = output
        self._thread_queue = queue
        self._json_algo_file = filename
        self._popen = None

    def stop(self):
        """ stop thread """
        self._output = None
        self._thread_queue = None
        if self._popen is not None:
            proc = self._popen
            self._kill(proc.pid)
            proc.stdout.close()

    def _kill(self, proc_pid):
        try:
            process = psutil.Process(proc_pid)
            for proc in process.children(recursive=True):
                proc.kill()
            process.kill()
        except Exception as ex:  # pylint: disable=broad-except
            if self._output is not None:
                self._output.write_line(
                    'Process kill has failed: {}'.format(str(ex)))

    def run(self):
        input_file = None
        output_file = None
        temp_input = False
        try:
            qiskit_chemistry_directory = os.path.dirname(os.path.realpath(__file__))
            qiskit_chemistry_directory = os.path.abspath(
                os.path.join(qiskit_chemistry_directory, '../command_line'))
            input_file = self.model.get_filename()
            if input_file is None or self.model.is_modified():
                f_d, input_file = tempfile.mkstemp(suffix='.in')
                os.close(f_d)
                temp_input = True
                self.model.save_to_file(input_file)

            startupinfo = None
            process_name = psutil.Process().exe()
            if not process_name:
                process_name = 'python'
            else:
                if sys.platform == 'win32' and process_name.endswith('pythonw.exe'):
                    path = os.path.dirname(process_name)
                    files = [f for f in os.listdir(path) if f != 'pythonw.exe' and f.startswith(
                        'python') and f.endswith('.exe')]
                    # sort reverse to have the python versions first: python3.exe before python2.exe
                    files = sorted(files, key=str.lower, reverse=True)
                    new_process = None
                    for file in files:
                        proc = os.path.join(path, file)
                        if os.path.isfile(proc):
                            # python.exe takes precedence
                            if file.lower() == 'python.exe':
                                new_process = proc
                                break

                            # use first found
                            if new_process is None:
                                new_process = proc

                    if new_process is not None:
                        startupinfo = subprocess.STARTUPINFO()
                        startupinfo.dwFlags = subprocess.STARTF_USESHOWWINDOW
                        startupinfo.wShowWindow = subprocess.SW_HIDE
                        process_name = new_process

            input_array = [process_name, qiskit_chemistry_directory, input_file]
            if self._json_algo_file:
                input_array.extend(['-jo', self._json_algo_file])
            else:
                f_d, output_file = tempfile.mkstemp(suffix='.out')
                os.close(f_d)
                input_array.extend(['-o', output_file])

            if self._output is not None and logger.getEffectiveLevel() == logging.DEBUG:
                self._output.write('Process: {}\n'.format(process_name))

            self._popen = subprocess.Popen(input_array,
                                           stdin=subprocess.DEVNULL,
                                           stdout=subprocess.PIPE,
                                           stderr=subprocess.STDOUT,
                                           startupinfo=startupinfo)
            if self._thread_queue is not None:
                self._thread_queue.put(GUIProvider.START)

            for line in io.TextIOWrapper(self._popen.stdout, encoding='utf-8', newline=''):
                if self._output is not None:
                    if platform.system() == "Windows":
                        line = line.replace('\r\n', '\n')

                    self._output.write(line)

            self._popen.stdout.close()
            self._popen.wait()
        except Exception as ex:  # pylint: disable=broad-except
            if self._output is not None:
                self._output.write('Process has failed: {}'.format(exception_to_string(ex)))
        finally:
            self._popen = None
            if self._thread_queue is not None:
                self._thread_queue.put(GUIProvider.STOP)
            try:
                if temp_input and input_file is not None:
                    os.remove(input_file)

                input_file = None
            finally:
                if output_file is not None:
                    os.remove(output_file)
                    output_file = None
