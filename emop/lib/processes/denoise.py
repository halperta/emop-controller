import collections
import os
import re
from emop.lib.emop_base import EmopBase
from emop.lib.processes.processes_base import ProcessesBase


class Denoise(ProcessesBase):

    def __init__(self, job):
        super(self.__class__, self).__init__(job)
        self.home = self.job.settings.denoise_home
        self.executable = os.path.join(self.home, "deNoise_Post.py")
        # This adds a trailing /
        self.xml_file_dir = os.path.join(self.job.output_dir, '')
        self.xml_filename = os.path.basename(self.job.xml_file)

    def run(self):
        Results = collections.namedtuple('Results', ['stdout', 'stderr', 'exitcode'])

        if not self.job.xml_file or not os.path.isfile(self.job.xml_file):
            stderr = "Could not find XML file: %s" % self.job.xml_file
            return Results(stdout=None, stderr=stderr, exitcode=1)

        cmd = ["python", self.executable, "-p", self.xml_file_dir, "-n", self.xml_filename]
        proc = EmopBase.exec_cmd(cmd)

        if proc.exitcode != 0:
            return Results(stdout=proc.stdout, stderr=proc.stderr, exitcode=proc.exitcode)

        out = proc.stdout
        noisemsr_match = re.search("NOISEMEASURE: ([0-9.]+)", out)
        if noisemsr_match:
            value = noisemsr_match.group(1)
            self.job.postproc_result.pp_noisemsr = value

        return Results(stdout=None, stderr=None, exitcode=0)
