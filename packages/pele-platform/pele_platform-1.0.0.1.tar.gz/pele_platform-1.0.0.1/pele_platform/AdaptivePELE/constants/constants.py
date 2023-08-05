from __future__ import absolute_import, division, print_function, unicode_literals
import os
import socket
import pele_platform.constants as cs
machine = socket.getfqdn()

print("MACHINE", machine)
if "bsccv" in machine:
    PELE_EXECUTABLE = "/data/EAPM/PELE/PELE++/bin/rev12360/Pele_rev12360_mpi"
    DATA_FOLDER = "/data/EAPM/PELE/PELE++/data/rev12360/Data"
    DOCUMENTS_FOLDER = "/data/EAPM/PELE/PELE++/Documents/rev12360"

    PYTHON = "/data2/apps/PYTHON/2.7.5/bin/python2.7"

elif "mn.bsc" in machine:
    PELE_EXECUTABLE = "/gpfs/projects/bsc72/PELE++/nord/rev090518/bin/PELE-1.5_mpi"
    DATA_FOLDER = "/gpfs/projects/bsc72/PELE++/nord/rev090518/Data"
    DOCUMENTS_FOLDER = "/gpfs/projects/bsc72/PELE++/nord/rev090518/Documents"
    PYTHON = "python"
    

elif "bsc.mn" in machine:
    PELE_EXECUTABLE = "/gpfs/projects/bsc72/PELE++/mniv/rev090518/bin/PELE-1.5_mpi"
    DATA_FOLDER = "/gpfs/projects/bsc72/PELE++/mniv/rev090518/Data"
    DOCUMENTS_FOLDER = "/gpfs/projects/bsc72/PELE++/mniv/rev090518/Documents"

elif machine == "bscls309":
    PELE_EXECUTABLE = "/home/jgilaber/PELE/PELE-1.5/bin/PELE-1.5_mpi"
    DATA_FOLDER = "/home/jgilaber/PELE/PELE-1.5/Data"
    DOCUMENTS_FOLDER = "/home/jgilaber/PELE/PELE-1.5/Documents"
else:
    PELE_EXECUTABLE = cs.PELE_BIN
    DATA_FOLDER = os.path.join(cs.PELE, "Data")
    DOCUMENTS_FOLDER = os.path.join(cs.PELE, "Documents")


inputFileTemplate = "{ \"files\" : [ { \"path\" : \"%s\" } ] }"
trajectoryBasename = "*traj*"


class OutputPathConstants():
    """
        Class with constants that depend on the outputPath
    """
    def __init__(self, outputPath):
        self.originalControlFile = ""
        self.epochOutputPathTempletized = ""
        self.clusteringOutputDir = ""
        self.clusteringOutputObject = ""
        self.tmpInitialStructuresTemplate = ""
        self.tmpControlFilename = ""
        self.tmpInitialStructuresEquilibrationTemplate = ""
        self.tmpControlFilenameEqulibration = ""
        self.buildConstants(outputPath)

    def buildConstants(self, outputPath):
        self.buildOutputPathConstants(outputPath)

        self.tmpFolder = "tmp_" + outputPath.replace("/", "_")

        self.buildTmpFolderConstants(self.tmpFolder)

    def buildOutputPathConstants(self, outputPath):
        self.originalControlFile = os.path.join(outputPath, "originalControlFile.conf")
        self.epochOutputPathTempletized = os.path.join(outputPath, "%d")
        self.clusteringOutputDir = os.path.join(self.epochOutputPathTempletized, "clustering")
        self.clusteringOutputObject = os.path.join(self.clusteringOutputDir, "object.pkl")
        self.topologyFile = os.path.join(outputPath, "topology.pdb")

    def buildTmpFolderConstants(self, tmpFolder):
        self.tmpInitialStructuresTemplate = tmpFolder+"/initial_%d_%d.pdb"
        self.tmpInitialStructuresEquilibrationTemplate = tmpFolder+"/initial_equilibration_%d.pdb"
        self.tmpControlFilename = tmpFolder+"/controlFile%d.conf"
        self.tmpControlFilenameEqulibration = tmpFolder+"/controlFile_equilibration_%d.conf"
