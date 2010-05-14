#!/usr/bin/env python
import math
import lsst.pex.harness.stage as harnessStage

from lsst.pex.logging import Log

import lsst.pex.policy as pexPolicy
import lsst.ip.isr as ipIsr

class IsrDarkStageParallel(harnessStage.ParallelProcessing):
    """
    Description:

    Policy Dictionary:

    Clipboard Input:

    ClipboardOutput:
    """
    def setup(self):
        self.log = Log(self.log, "IsrDarkStage - parallel")

        policyFile = pexPolicy.DefaultPolicyFile("ip_pipeline", "IsrDarkStageDictionary.paf", "policy")
        defPolicy = pexPolicy.Policy.createPolicy(policyFile, policyFile.getRepositoryPath())

        if self.policy is None:
            self.policy = pexPolicy.Policy()
        self.policy.mergeDefaults(defPolicy)

    def process(self, clipboard):
        """
        """
        self.log.log(Log.INFO, "Doing dark subtraction.")
        
        #grab exposure and dark from clipboard
        darkexposure = clipboard.get(self.policy.getString("inputKeys.darkexposure"))
        exposure = clipboard.get(self.policy.getString("inputKeys.exposure"))
        darkscaling = darkexposure.getMetadata().get(self.policy.getString("parameters.darkscaleKeyword"))
        expscaling = exposure.getMetadata().get(self.policy.getString("parameters.exposurescaleKeyword"))
        ipIsr.darkCorrection(exposure, darkexposure, float(expscaling),
                float(darkscaling))
        ipIsr.updateVariance(exposure)

        #output products
        clipboard.put(self.policy.get("outputKeys.darkSubtractedExposure"), exposure)
        
class IsrDarkStage(harnessStage.Stage):
    parallelClass = IsrDarkStageParallel

