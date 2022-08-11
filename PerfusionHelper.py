import logging
import os

import vtk

import slicer
from slicer.ScriptedLoadableModule import *
from slicer.util import VTKObservationMixin


#
# PerfusionHelper
#


class PerfusionHelper(ScriptedLoadableModule):
    """Uses ScriptedLoadableModule base class, available at:
    https://github.com/Slicer/Slicer/blob/master/Base/Python/slicer/ScriptedLoadableModule.py
    """

    def __init__(self, parent):
        ScriptedLoadableModule.__init__(self, parent)
        self.parent.title = (
            "PerfusionHelper"  # TODO: make this more human readable by adding spaces
        )
        self.parent.categories = ["MikeTools"]
        self.parent.dependencies = [
            "Elastix"
        ]  # TODO: add here list of module names that this module requires
        self.parent.contributors = [
            "Mike Bindschadler (Seattle Children's Hospital)"
        ]  #
        # TODO: update with short description of the module and a link to online module documentation
        self.parent.helpText = """
This is an example of scripted loadable module bundled in an extension.
See more information in <a href="https://github.com/organization/projectname#PerfusionHelper">module documentation</a>.
"""
        self.parent.acknowledgementText = """
This file was originally developed by Mike Bindschadler and was funded by Seattle Children's Hospital.
"""


'''
        # Additional initialization step after application startup is complete
        slicer.app.connect("startupCompleted()", registerSampleData)


#
# Register sample data sets in Sample Data module
#


def registerSampleData():
    """
    Add data sets to Sample Data module.
    """
    # It is always recommended to provide sample data for users to make it easy to try the module,
    # but if no sample data is available then this method (and associated startupCompeted signal connection) can be removed.

    import SampleData

    iconsPath = os.path.join(os.path.dirname(__file__), "Resources/Icons")

    # To ensure that the source code repository remains small (can be downloaded and installed quickly)
    # it is recommended to store data sets that are larger than a few MB in a Github release.

    # PerfusionHelper1
    SampleData.SampleDataLogic.registerCustomSampleDataSource(
        # Category and sample name displayed in Sample Data module
        category="PerfusionHelper",
        sampleName="PerfusionHelper1",
        # Thumbnail should have size of approximately 260x280 pixels and stored in Resources/Icons folder.
        # It can be created by Screen Capture module, "Capture all views" option enabled, "Number of images" set to "Single".
        thumbnailFileName=os.path.join(iconsPath, "PerfusionHelper1.png"),
        # Download URL and target file name
        uris="https://github.com/Slicer/SlicerTestingData/releases/download/SHA256/998cb522173839c78657f4bc0ea907cea09fd04e44601f17c82ea27927937b95",
        fileNames="PerfusionHelper1.nrrd",
        # Checksum to ensure file integrity. Can be computed by this command:
        #  import hashlib; print(hashlib.sha256(open(filename, "rb").read()).hexdigest())
        checksums="SHA256:998cb522173839c78657f4bc0ea907cea09fd04e44601f17c82ea27927937b95",
        # This node name will be used when the data set is loaded
        nodeNames="PerfusionHelper1",
    )

    # PerfusionHelper2
    SampleData.SampleDataLogic.registerCustomSampleDataSource(
        # Category and sample name displayed in Sample Data module
        category="PerfusionHelper",
        sampleName="PerfusionHelper2",
        thumbnailFileName=os.path.join(iconsPath, "PerfusionHelper2.png"),
        # Download URL and target file name
        uris="https://github.com/Slicer/SlicerTestingData/releases/download/SHA256/1a64f3f422eb3d1c9b093d1a18da354b13bcf307907c66317e2463ee530b7a97",
        fileNames="PerfusionHelper2.nrrd",
        checksums="SHA256:1a64f3f422eb3d1c9b093d1a18da354b13bcf307907c66317e2463ee530b7a97",
        # This node name will be used when the data set is loaded
        nodeNames="PerfusionHelper2",
    )
'''

#
# PerfusionHelperWidget
#


class PerfusionHelperWidget(ScriptedLoadableModuleWidget, VTKObservationMixin):
    """Uses ScriptedLoadableModuleWidget base class, available at:
    https://github.com/Slicer/Slicer/blob/master/Base/Python/slicer/ScriptedLoadableModule.py
    """

    def __init__(self, parent=None):
        """
        Called when the user opens the module the first time and the widget is initialized.
        """
        ScriptedLoadableModuleWidget.__init__(self, parent)
        VTKObservationMixin.__init__(self)  # needed for parameter node observation
        self.logic = None
        self._parameterNode = None
        self._updatingGUIFromParameterNode = False

    def setup(self):
        """
        Called when the user opens the module the first time and the widget is initialized.
        """
        ScriptedLoadableModuleWidget.setup(self)

        # Load widget from .ui file (created by Qt Designer).
        # Additional widgets can be instantiated manually and added to self.layout.
        uiWidget = slicer.util.loadUI(self.resourcePath("UI/PerfusionHelper.ui"))
        self.layout.addWidget(uiWidget)
        self.ui = slicer.util.childWidgetVariables(uiWidget)

        # Set scene in MRML widgets. Make sure that in Qt designer the top-level qMRMLWidget's
        # "mrmlSceneChanged(vtkMRMLScene*)" signal in is connected to each MRML widget's.
        # "setMRMLScene(vtkMRMLScene*)" slot.
        uiWidget.setMRMLScene(slicer.mrmlScene)

        # Create logic class. Logic implements all computations that should be possible to run
        # in batch mode, without a graphical user interface.
        self.logic = PerfusionHelperLogic()

        # Connections

        # These connections ensure that we update parameter node when scene is closed
        self.addObserver(
            slicer.mrmlScene, slicer.mrmlScene.StartCloseEvent, self.onSceneStartClose
        )
        self.addObserver(
            slicer.mrmlScene, slicer.mrmlScene.EndCloseEvent, self.onSceneEndClose
        )

        # These connections ensure that whenever user changes some settings on the GUI, that is saved in the MRML scene
        # (in the selected parameter node).
        self.ui.GatherTagsInputSequenceSelector.connect(
            "currentNodeChanged(vtkMRMLNode*)", self.updateParameterNodeFromGUI
        )
        self.ui.InputRegisteredSequenceSelector.connect(
            "currentNodeChanged(vtkMRMLNode*)", self.updateParameterNodeFromGUI
        )
        self.ui.OutputRegisteredSequenceSelector.connect(
            "currentNodeChanged(vtkMRMLNode*)", self.updateParameterNodeFromGUI
        )
        self.ui.T1RegSequenceInputSelector.connect(
            "currentNodeChanged(vtkMRMLNode*)", self.updateParameterNodeFromGUI
        )
        self.ui.T1RegT1Selector.connect(
            "currentNodeChanged(vtkMRMLNode*)", self.updateParameterNodeFromGUI
        )
        self.ui.TransferTagsInputSequenceSelector.connect(
            "currentNodeChanged(vtkMRMLNode*)", self.updateParameterNodeFromGUI
        )
        self.ui.TransferTagsDestinationSequenceSelector.connect(
            "currentNodeChanged(vtkMRMLNode*)", self.updateParameterNodeFromGUI
        )
        self.ui.T1RegOutputTransformSelector.connect(
            "currentNodeChanged(vtkMRMLNode*)", self.updateParameterNodeFromGUI
        )
        self.ui.RegistrationStrategyComboBox.connect(
            "currentIndexChanged(int)", self.updateParameterNodeFromGUI
        )
        self.ui.HardenTransformCheckBox.connect(
            "stateChanged(int)", self.updateParameterNodeFromGUI
        )

        # Buttons
        self.ui.GatherTagsFromDICOMButton.connect(
            "clicked(bool)", self.onGatherTagsFromDICOMButtonClick
        )
        self.ui.TransferTagsButton.connect(
            "clicked(bool)", self.onTransferTagsButtonClick
        )
        self.ui.RunSequenceRegistrationButton.connect(
            "clicked(bool)", self.onRunSequenceRegistrationButtonClick
        )
        self.ui.RegisterT1Button.connect("clicked(bool)", self.onRegisterT1ButtonClick)

        # Initialize registration strategy choice combobox
        self.ui.RegistrationStrategyComboBox.clear()
        self.ui.RegistrationStrategyComboBox.addItems(["BRAINS", "Elastix"])

        # Make sure parameter node is initialized (needed for module reload)
        self.initializeParameterNode()

    def cleanup(self):
        """
        Called when the application closes and the module widget is destroyed.
        """
        self.removeObservers()

    def enter(self):
        """
        Called each time the user opens this module.
        """
        # Make sure parameter node exists and observed
        self.initializeParameterNode()

    def exit(self):
        """
        Called each time the user opens a different module.
        """
        # Do not react to parameter node changes (GUI wlil be updated when the user enters into the module)
        self.removeObserver(
            self._parameterNode,
            vtk.vtkCommand.ModifiedEvent,
            self.updateGUIFromParameterNode,
        )

    def onSceneStartClose(self, caller, event):
        """
        Called just before the scene is closed.
        """
        # Parameter node will be reset, do not use it anymore
        self.setParameterNode(None)

    def onSceneEndClose(self, caller, event):
        """
        Called just after the scene is closed.
        """
        # If this module is shown while the scene is closed then recreate a new parameter node immediately
        if self.parent.isEntered:
            self.initializeParameterNode()

    def initializeParameterNode(self):
        """
        Ensure parameter node exists and observed.
        """
        # Parameter node stores all user choices in parameter values, node selections, etc.
        # so that when the scene is saved and reloaded, these settings are restored.

        self.setParameterNode(self.logic.getParameterNode())

        # Any automatic initialization could go here (auto-selecting nodes from the scene, for example)

    def setParameterNode(self, inputParameterNode):
        """
        Set and observe parameter node.
        Observation is needed because when the parameter node is changed then the GUI must be updated immediately.
        """

        if inputParameterNode:
            self.logic.setDefaultParameters(inputParameterNode)

        # Unobserve previously selected parameter node and add an observer to the newly selected.
        # Changes of parameter node are observed so that whenever parameters are changed by a script or any other module
        # those are reflected immediately in the GUI.
        if self._parameterNode is not None:
            self.removeObserver(
                self._parameterNode,
                vtk.vtkCommand.ModifiedEvent,
                self.updateGUIFromParameterNode,
            )
        self._parameterNode = inputParameterNode
        if self._parameterNode is not None:
            self.addObserver(
                self._parameterNode,
                vtk.vtkCommand.ModifiedEvent,
                self.updateGUIFromParameterNode,
            )

        # Initial GUI update
        self.updateGUIFromParameterNode()

    def updateGUIFromParameterNode(self, caller=None, event=None):
        """
        This method is called whenever parameter node is changed.
        The module GUI is updated to show the current state of the parameter node.
        """

        if self._parameterNode is None or self._updatingGUIFromParameterNode:
            return

        # Make sure GUI changes do not call updateParameterNodeFromGUI (it could cause infinite loop)
        self._updatingGUIFromParameterNode = True

        pn = self._parameterNode
        ## Update node selectors and sliders
        self.ui.GatherTagsInputSequenceSelector.setCurrentNode(
            pn.GetNodeReference("GatherTagsInputSequence")
        )
        self.ui.InputRegisteredSequenceSelector.setCurrentNode(
            pn.GetNodeReference("InputRegisteredSequence")
        )
        self.ui.OutputRegisteredSequenceSelector.setCurrentNode(
            pn.GetNodeReference("OutputRegisteredSequence")
        )
        self.ui.T1RegSequenceInputSelector.setCurrentNode(
            pn.GetNodeReference("T1RegSequenceInput")
        )
        self.ui.T1RegT1Selector.setCurrentNode(pn.GetNodeReference("T1Node"))
        self.ui.T1RegBrainMaskSelector.setCurrentNode(
            pn.GetNodeReference("T1BrainMask")
        )
        self.ui.T1RegOutputTransformSelector.setCurrentNode(
            pn.GetNodeReference("T1RegTransform")
        )
        self.ui.TransferTagsInputSequenceSelector.setCurrentNode(
            pn.GetNodeReference("TransferTagsInputSequence")
        )
        self.ui.TransferTagsDestinationSequenceSelector.setCurrentNode(
            pn.GetNodeReference("TransferTagsDestinationSequence")
        )

        ##  Update buttons states and tooltips
        # Gather tags section
        if self._parameterNode.GetNodeReference("GatherTagsInputSequence"):
            self.ui.GatherTagsFromDICOMButton.toolTip = (
                "Gather and apply perfusion tags to input sequence"
            )
            self.ui.GatherTagsFromDICOMButton.enabled = True
        else:
            self.ui.GatherTagsFromDICOMButton.toolTip = (
                "Select input image volume sequence to enable tagging"
            )
            self.ui.GatherTagsFromDICOMButton.enabled = False
        # Sequence registration section
        if pn.GetNodeReference("InputRegisteredSequence"):
            self.ui.RunSequenceRegistrationButton.toolTip = (
                "Run sequence registration using default rigid registration settings"
            )
            self.ui.RunSequenceRegistrationButton.enabled = True
        else:
            self.ui.RunSequenceRegistrationButton.toolTip = (
                "Select sequence to register to enable registration"
            )
            self.ui.RunSequenceRegistrationButton.enabled = False
        # Transfer tags section
        if pn.GetNodeReference("TransferTagsInputSequence") and pn.GetNodeReference(
            "TransferTagsDestinationSequence"
        ):
            self.ui.TransferTagsButton.toolTip = (
                "Transfer all attribute tags from source to destination"
            )
            self.ui.TransferTagsButton.enabled = True
        else:
            self.ui.TransferTagsButton.toolTip = (
                "Select both source and destination sequences to enable tag transfer"
            )
            self.ui.TransferTagsButton.enabled = False
        # T1 registration section
        if pn.GetNodeReference("T1Node") and pn.GetNodeReference("T1RegSequenceInput"):
            self.ui.RegisterT1Button.toolTip = "Register T1 to first frame of sequence"
            self.ui.RegisterT1Button.enabled = True
        else:
            self.ui.RegisterT1Button.toolTip = (
                "Select a T1 and an image sequence to enable registration"
            )
            self.ui.RegisterT1Button.enabled = False

        ## Registration strategy combobox
        strategyOptionsList = [
            self.ui.RegistrationStrategyComboBox.itemText(idx)
            for idx in range(self.ui.RegistrationStrategyComboBox.count)
        ]
        if pn.GetParameter("RegistrationStrategy") in strategyOptionsList:
            newIdx = strategyOptionsList.index(pn.GetParameter("RegistrationStrategy"))
            self.ui.RegistrationStrategyComboBox.setCurrentIndex(newIdx)
        else:
            self.ui.RegistrationStrategyComboBox.setCurrentIndex(0)
            raise Exception("Unknown registration strategy %s in parameter node!")

        ## Checkbox
        self.ui.HardenTransformCheckBox.checked = (
            pn.GetParameter("HardenTransformChecked") == "1"
        )

        # All the GUI updates are done
        self._updatingGUIFromParameterNode = False

    def updateParameterNodeFromGUI(self, caller=None, event=None):
        """
        This method is called when the user makes any change in the GUI.
        The changes are saved into the parameter node (so that they are restored when the scene is saved and loaded).
        """

        if self._parameterNode is None or self._updatingGUIFromParameterNode:
            return

        wasModified = (
            self._parameterNode.StartModify()
        )  # Modify all properties in a single batch
        pn = self._parameterNode

        # Checkbox
        pn.SetParameter(
            "HardenTransformChecked",
            "1" if self.ui.HardenTransformCheckBox.checked else "0",
        )

        # Set node references from selectors
        pn.SetNodeReferenceID(
            "GatherTagsInputSequence",
            self.ui.GatherTagsInputSequenceSelector.currentNodeID,
        )
        pn.SetNodeReferenceID(
            "InputRegisteredSequence",
            self.ui.InputRegisteredSequenceSelector.currentNodeID,
        )
        pn.SetNodeReferenceID(
            "OutputRegisteredSequence",
            self.ui.OutputRegisteredSequenceSelector.currentNodeID,
        )
        pn.SetNodeReferenceID(
            "T1RegSequenceInput", self.ui.T1RegSequenceInputSelector.currentNodeID
        )
        pn.SetNodeReferenceID("T1Node", self.ui.T1RegT1Selector.currentNodeID)
        pn.SetNodeReferenceID(
            "T1BrainMask", self.ui.T1RegBrainMaskSelector.currentNodeID
        )
        pn.SetNodeReferenceID(
            "T1RegTransform", self.ui.T1RegOutputTransformSelector.currentNodeID
        )
        pn.SetNodeReferenceID(
            "TransferTagsInputSequence",
            self.ui.TransferTagsInputSequenceSelector.currentNodeID,
        )
        pn.SetNodeReferenceID(
            "TransferTagsDestinationSequence",
            self.ui.TransferTagsDestinationSequenceSelector.currentNodeID,
        )
        pn.SetParameter(
            "RegistrationStrategy", self.ui.RegistrationStrategyComboBox.currentText
        )

        self._parameterNode.EndModify(wasModified)

    def onGatherTagsFromDICOMButtonClick(self):
        """For input sequence, gather perfustion related tags from DICOM header"""
        seqNode = self.ui.GatherTagsInputSequenceSelector.currentNode()
        if not seqNode:
            slicer.util.errorDisplay("No input sequence selected!")

        errorCode, errorMsg = self.logic.gatherTagsFromDICOMTag(seqNode)
        if errorCode > 0:
            slicer.util.errorDisplay(errorMsg)
            raise Exception(errorMsg)

    def onTransferTagsButtonClick(self):
        """Transfer all attributes from source to destination node"""
        sourceNode = self.ui.TransferTagsInputSequenceSelector.currentNode()
        destNode = self.ui.TransferTagsDestinationSequenceSelector.currentNode()
        self.logic.transferTags(sourceNode, destNode)
        slicer.util.infoDisplay("Tags successfully transferred!")

    def onRunSequenceRegistrationButtonClick(self):
        """Run sequence registration using "generic rigid (all)" preset"""
        inputSequence = self.ui.InputRegisteredSequenceSelector.currentNode()
        outputSequence = self.ui.OutputRegisteredSequenceSelector.currentNode()
        if outputSequence is None:
            outSeqName = slicer.mrmlScene.GenerateUniqueName("RegisteredSequence")
            outputSequence = slicer.mrmlScene.AddNewNodeByClass(
                "vtkMRMLSequenceNode", outSeqName
            )
            self.ui.OutputRegisteredSequenceSelector.setCurrentNode(outputSequence)
        outputTransformSequence = None  # TODO add selector for this
        outputs = self.logic.runSequenceRegistration(
            inputSequence, outputSequence, outputTransformSequence
        )
        # Announce when finished
        slicer.util.infoDisplay("Sequence registration finished!")
        # Transfer tags to registered version
        self.logic.transferTags(inputSequence, outputSequence)
        # Set the output as the suggested sequence for T1 registration
        self._parameterNode.SetNodeReferenceID(
            "T1RegSequenceInput", outputSequence.GetID()
        )

    def onRegisterT1ButtonClick(self):
        """Do rigid registration of T1 to current frame of sequence"""
        T1node = self.ui.T1RegT1Selector.currentNode()
        seqNode = self.ui.T1RegSequenceInputSelector.currentNode()
        brainMaskNode = self.ui.T1RegBrainMaskSelector.currentNode()
        outputTransformNode = self.ui.T1RegOutputTransformSelector.currentNode()
        strategy = self.ui.RegistrationStrategyComboBox.currentText
        outputTransformNode = self.logic.registerT1ToSequence(
            T1node, seqNode, brainMaskNode, outputTransformNode, strategy
        )
        # Set output transform node (in case it was just created)
        self._parameterNode.SetNodeReferenceID(
            "T1RegTransform", outputTransformNode.GetID()
        )
        # Apply transform to T1 node and brain mask
        T1node.SetAndObserveTransformNodeID(outputTransformNode.GetID())
        if brainMaskNode:
            brainMaskNode.SetAndObserveTransformNodeID(outputTransformNode.GetID())
        # Harden transform if requested
        if self.ui.HardenTransformCheckBox.checked:
            T1node.HardenTransform()
            if brainMaskNode:
                brainMaskNode.HardenTransform()
        self.updateGUIFromParameterNode()

    def onApplyButton(self):
        """
        VESTIGAL!
        Run processing when user clicks "Apply" button.
        """
        with slicer.util.tryWithErrorDisplay(
            "Failed to compute results.", waitCursor=True
        ):

            # Compute output
            self.logic.process(self.ui.inputSelector.currentNode())


#
# PerfusionHelperLogic
#


class PerfusionHelperLogic(ScriptedLoadableModuleLogic):
    """This class should implement all the actual
    computation done by your module.  The interface
    should be such that other python code can import
    this class and make use of the functionality without
    requiring an instance of the Widget.
    Uses ScriptedLoadableModuleLogic base class, available at:
    https://github.com/Slicer/Slicer/blob/master/Base/Python/slicer/ScriptedLoadableModule.py
    """

    def __init__(self):
        """
        Called when the logic class is instantiated. Can be used for initializing member variables.
        """
        ScriptedLoadableModuleLogic.__init__(self)
        # Set to delete temporary files created during elastix registration
        self.deleteTempElastixFiles = False  # TODO: change to true when working!

    def setDefaultParameters(self, parameterNode):
        """
        Initialize parameter node with default settings.
        """
        if not parameterNode.GetParameter("RegistrationStrategy"):
            parameterNode.SetParameter("RegistrationStrategy", "BRAINS")
        # if not parameterNode.GetParameter("Threshold"):
        #     parameterNode.SetParameter("Threshold", "100.0")
        # if not parameterNode.GetParameter("Invert"):
        #     parameterNode.SetParameter("Invert", "false")
        pass

    def runSequenceRegistration(
        self, inputSequence, outputSequence, outputTransformSequence=None
    ):
        """ """
        generic_rigid_preset_idx = 1
        import SequenceRegistration

        seqRegLogic = SequenceRegistration.SequenceRegistrationLogic()
        seqRegLogic.registerVolumeSequence(
            inputSequence,
            outputSequence,
            outputTransformSequence,
            fixedVolumeItemNumber=0,
            computeMovingToFixedTransform=True,
            presetIndex=generic_rigid_preset_idx,
            startFrameIndex=0,
            endFrameIndex=None,
        )
        pass

    def registerT1ToSequence(
        self, T1node, seqNode, brainMaskNode, outputTransformNode, strategy
    ):
        """ """
        # Get proxy node for desired sequence node
        browserNode = (
            slicer.modules.sequences.logic().GetFirstBrowserNodeForSequenceNode(seqNode)
        )
        proxNode = browserNode.GetProxyNode(seqNode)
        fixedVolumeMask = None  # no mask on sequence
        if strategy == "BRAINS":
            outputTransformNode = self.runBrainsRegistration(
                proxNode, T1node, outputTransformNode
            )
        elif strategy == "Elastix":
            outputTransformNode = self.runElastixRegistration(
                proxNode,
                T1node,
                fixedVolumeMask,
                brainMaskNode,
                outputTransformNode,
                prealigned=True,
            )
        return outputTransformNode

    def transferTags(self, sourceNode, destNode):
        """Transfer all attributes from source node to destination node"""
        for attrName in sourceNode.GetAttributeNames():
            destNode.SetAttribute(attrName, sourceNode.GetAttribute(attrName))

    def gatherTagsFromDICOMTag(self, inputSequenceNode):
        """
        Gather perfusion-related tags needed by DSCMRIAnalysis module based by getting header
        from instance UID and add them as attributes to the input sequence node.
        If  there is no instance UID attribute for this sequence, return an error code!

        """
        seqNode = inputSequenceNode
        if seqNode is None:
            errorCode, errorMsg = (1, "Input sequence is None!")
            return errorCode, errorMsg
        # Get proxy node for desired sequence node
        browserNode = (
            slicer.modules.sequences.logic().GetFirstBrowserNodeForSequenceNode(seqNode)
        )
        proxNode = browserNode.GetProxyNode(seqNode)
        if not "DICOM.instanceUIDs" in proxNode.GetAttributeNames():
            errorCode, errorMsg = (
                2,
                "Image volumes in sequence do not have 'DICOM.instanceUIDs as attributes! Cannot retrieve other tag data without a reference to the DICOM header!",
            )
            return errorCode, errorMsg
        # Get sop instance UIDs list from sequence proxy node attribute
        instUIDs = proxNode.GetAttribute("DICOM.instanceUIDs").split()
        # Get first DICOM file name and location from Slicer's DICOM database
        dcmFileName = slicer.dicomDatabase.fileForInstance(instUIDs[0])
        # Read header metadata into pydicom data set
        import pydicom

        ds = pydicom.dcmread(dcmFileName)
        # Gather needed parameters
        echoTime = ds.EchoTime
        flipAngle = ds.FlipAngle
        repetitionTime = ds.RepetitionTime
        # Make list of needed frame labels
        frameLabels = " ".join(
            [
                "%i" % (idx * repetitionTime)
                for idx in range(seqNode.GetNumberOfDataNodes())
            ]
        )
        # Add attributes to Sequence node (note that conversion is necessary from pydicom output to regular strings)
        seqNode.SetAttribute("MultiVolume.DICOM.EchoTime", "%0.1f" % echoTime)
        seqNode.SetAttribute("MultiVolume.DICOM.FlipAngle", "%0.1f" % flipAngle)
        seqNode.SetAttribute("MultiVolume.FrameLabels", frameLabels)
        seqNode.SetAttribute(
            "MultiVolume.FrameIdentifyingDICOMTagName", "AcquisitionTime"
        )

        errorCode, errorMsg = (0, "")

        slicer.util.messageBox(
            "Perfusion tags successfully applied to volume sequence!"
        )

        # import time
        # startTime = time.time()
        # logging.info("Processing started")
        #
        #
        # stopTime = time.time()
        # logging.info(f"Processing completed in {stopTime-startTime:.2f} seconds")
        return errorCode, errorMsg

    def newNode(self, nodeClass, baseNodeName):
        # Convenience function for repeated code used for generating unique names
        # AddNewNodeByClass is supposed to do this according to the docs, but it doesn't
        nodeName = slicer.mrmlScene.GenerateUniqueName(baseNodeName)
        node = slicer.mrmlScene.AddNewNodeByClass(nodeClass, nodeName)
        return node

    def runBrainsRegistration(self, fixed, moving, outputTransform=None):
        """Run registration without any fancy stuff, assuming a fairly close match between volumes."""
        if outputTransform is None:
            outputTransform = slicer.mrmlScene.AddNewNodeByClass(
                "vtkMRMLLinearTransformNode",
                "_".join([fixed.GetName(), "to", moving.GetName(), "Transform"]),
            )
        parameters = {
            "fixedVolume": fixed,
            "movingVolume": moving,
            "samplingPercentage": 0.01,
            "linearTransform": outputTransform,
            "initializeTransformMode": "Off",  # assumes already close in physical space
            "useRigid": True,
        }
        slicer.cli.runSync(slicer.modules.brainsfit, None, parameters=parameters)
        return outputTransform

    def runElastixRegistration(
        self,
        fixedVolumeNode,
        movingVolumeNode,
        fixedVolumeMaskNode=None,
        movingVolumeMaskNode=None,
        elastixOutputTransform=None,
        prealigned=False,
        maskHasFalseHardEdge=False,
        Scales=None,
    ):
        """Run elastix-based registration and output the resulting transform as slicer linear
        transform node. If mask nodes are supplied, they are used and are not eroded by default. The
        parameter file used is created on the fly so that the user doesn't have to mess with the xml
        database file or find any file locations. Optional input flags affect creation of the parameter
        file:
        FlagName  --  Values(default)
        prealigned -- True/(False).  If False, images are centered via AutomaticTransformInitialization with "CenterOfGravity" method
                      If True, images are not centered, it is instead assumed that they are already close together in physical space
        maskHasFalseHardEdge -- True/(False). This controls whether ErodeMask is true or false. It has no effect if not
                                using mask volumes. If there is a false hard edge in either mask, then ErodeMask should be
                                true so that blurred versions are not influenced by this hard edge. If not, then it's better
                                to leave the full mask. In our standard use case, I expect the MR mask not to have hard false edges,
                                so the default is False
        Scales -- (None) or number.  If None, AutomaticScalesEstimation is used. If a number, then this number is used as the
                  Scales parameter, which controls how much rotation parameter value changes are considered relative to translation.
                  Automatic scales seem to fall in the ~7000-9000 range, and lower values allow more exploration of rotation. Manual
                  suggests never to go below 1000. I found cases where automate scales estimation failed, but 5000 worked well, so this
                  might be a reasonable thing to try if the auto case fails.
        """
        ### Implementation modified from Elastix.py from Elastix module ###
        if elastixOutputTransform is None:
            elastixOutputTransform = self.newNode(
                "vtkMRMLLinearTransformNode", "ElastixOutputTranform"
            )
        import Elastix, qt

        elastixLogic = Elastix.ElastixLogic()
        # Create temporary directory to hold volumes used for Elastix registration and registration results
        tempDir = elastixLogic.createTempDirectory()
        # Create inputs subdirectory
        inputDir = os.path.join(tempDir, "input")
        qt.QDir().mkpath(inputDir)
        # Create desired parameter file in this temp directory
        parameterFilePath = self.createElastixParameterFile(
            inputDir,
            prealigned=prealigned,
            maskHasFalseHardEdge=maskHasFalseHardEdge,
            Scales=Scales,
        )
        # Assemble command line parameters and save copies of inputs to input directory
        inputParamsElastix = []  # list to hold command line arguments
        self.addLog("Volume registration is started in working directory: " + tempDir)
        # Add input volumes
        inputVolumes = []
        inputVolumes.append([fixedVolumeNode, "fixed.mha", "-f"])
        inputVolumes.append([movingVolumeNode, "moving.mha", "-m"])
        inputVolumes.append([fixedVolumeMaskNode, "fixedMask.mha", "-fMask"])
        inputVolumes.append([movingVolumeMaskNode, "movingMask.mha", "-mMask"])
        for [volumeNode, filename, paramName] in inputVolumes:
            if not volumeNode:
                continue
            # Save original file paths
            originalFilePath = ""
            originalFilePaths = []
            volumeStorageNode = volumeNode.GetStorageNode()
            if volumeStorageNode:
                originalFilePath = volumeStorageNode.GetFileName()
                for fileIndex in range(volumeStorageNode.GetNumberOfFileNames()):
                    originalFilePaths.append(
                        volumeStorageNode.GetNthFileName(fileIndex)
                    )
            # Save to new location
            filePath = os.path.join(inputDir, filename)
            slicer.util.saveNode(volumeNode, filePath, {"useCompression": False})
            inputParamsElastix.append(paramName)
            inputParamsElastix.append(filePath)
            # Restore original file paths
            if volumeStorageNode:
                volumeStorageNode.ResetFileNameList()
                volumeStorageNode.SetFileName(originalFilePath)
                for fileIndex in range(volumeStorageNode.GetNumberOfFileNames()):
                    volumeStorageNode.AddFileName(originalFilePaths[fileIndex])
            else:
                # temporary storage node was created, remove it to restore original state
                volumeStorageNode = volumeNode.GetStorageNode()
                slicer.mrmlScene.RemoveNode(volumeStorageNode)
        # Specify output location
        resultTransformDir = os.path.join(tempDir, "result-transform")
        qt.QDir().mkpath(resultTransformDir)
        inputParamsElastix += ["-out", resultTransformDir]
        # Specify parameter file
        inputParamsElastix.append("-p")
        inputParamsElastix.append(parameterFilePath)
        # Run the registration!
        ep = elastixLogic.startElastix(inputParamsElastix)
        # ep.stdout.close()  # Needed or ep.wait() hangs forever
        # return_code = ep.wait() # returns when the process ends?
        elastixLogic.logProcessOutput(
            ep
        )  # if I don't do this line, the registration stalls at the start of resolution 0 unless I uncomment and run the previous two lines
        self.addLog(
            "\nRegistration complete, transform in:\n   %s" % resultTransformDir
        )
        # Import the resulting transform
        self.importElastixTransform(resultTransformDir, elastixOutputTransform)
        # Clean up temporary nodes/files
        if self.deleteTempElastixFiles:
            import shutil

            shutil.rmtree(tempDir)
        return elastixOutputTransform

    def importElastixTransform(self, resultTransformDir, outputTransformNode):
        import Elastix

        elastixLogic = Elastix.ElastixLogic()
        generalTransformFromParent = vtk.vtkGeneralTransform()
        transformFileName = (
            resultTransformDir + "/TransformParameters.0.txt"
        )  # would need to be adjusted if there were multiple parameters run!!!
        elastixLogic.readElastixLinearTransformToVTK(
            transformFileName, generalTransformFromParent
        )
        transformFromParentLinear = vtk.vtkTransform()
        if slicer.vtkMRMLTransformNode.IsGeneralTransformLinear(
            generalTransformFromParent, transformFromParentLinear
        ):
            outputTransformNode.SetMatrixTransformFromParent(
                transformFromParentLinear.GetMatrix()
            )
        else:
            outputTransformNode.SetAndObserveTransformFromParent(
                generalTransformFromParent
            )
            slicer.util.errorDisplay(
                "Imported Elastix transform was not linear!  Errors may ensue, because this is not the expected case"
            )
        elastixTransformFileImported = True

    def createElastixParameterFile(
        self, destDir, prealigned=False, maskHasFalseHardEdge=False, Scales=None
    ):
        """Create Elastix parameter file from scratch (so we don't have to mess with the XML presets or other things)"""  # TODO: add kwargs type argument to allow arbitrary modifications to the parameters
        p = {}
        # Parameters to modify if needed
        p["NumberOfResolutions"] = 6
        p[
            "AutomaticTransformInitializationMethod"
        ] = "Origins"  # likely to be true for our perfusion images
        if Scales is None:
            p["AutomaticScalesEstimation"] = "true"
        else:
            p["Scales"] = Scales  # 5000 is a good choice
        p["NumberOfHistogramBins"] = 64
        p["MaximumNumberOfIterations"] = 1000
        p["NumberOfSpatialSamples"] = 3000
        if prealigned:
            p["AutomaticTransformInitialization"] = "false"
        else:
            p["AutomaticTransformInitialization"] = "true"
        # Only relevant if using mask
        if maskHasFalseHardEdge:
            # If the mask abuts a false hard edge contained in an image (e.g. T1_cut or CT resampled, where there might be a false edge internal to the image)
            # then the mask should be eroded in blurred or downsampled images to avoid having the bad edge influence the registration
            p["ErodeMask"] = "true"
        else:
            # If there is no hard false edge in the image or if it is far from the mask ROI, then it is better
            # not to erode the mask
            p["ErodeMask"] = "false"
        #

        # This is the default image pyramid schedule for 6 resolutions
        # p['ImagePyramidSchedule'] = '32 32 32  16 16 16  8 8 8  4 4 4  2 2 2  1 1 1'

        # Standard parameters which shouldn't need to be modified
        p["FixedInternalImagePixelType"] = "float"
        p["MovingInternalImagePixelType"] = "float"
        p["Registration"] = "MultiResolutionRegistration"
        p["Interpolator"] = "LinearInterpolator"
        p["ResampleInterpolator"] = "FinalBSplineInterpolator"
        p["FinalBSplineInterpolationOrder"] = 3
        p["Resampler"] = "DefaultResampler"
        p["FixedImagePyramid"] = "FixedSmoothingImagePyramid"
        p["MovingImagePyramid"] = "MovingSmoothingImagePyramid"
        p["Optimizer"] = "AdaptiveStochasticGradientDescent"
        p["ASGDParameterEstimationMethod"] = "DisplacementDistribution"
        p["Transform"] = "EulerTransform"
        p["Metric"] = "AdvancedMattesMutualInformation"
        p["HowToCombineTransforms"] = "Compose"
        p["NewSamplesEveryIteration"] = "true"
        p["ImageSampler"] = "RandomCoordinate"
        p["DefaultPixelValue"] = 0
        p[
            "WriteResultImage"
        ] = "false"  # saves time because I am only extracting the transform
        p["ResultImagePixelType"] = "short"  # not used because no result image written
        p["ResultImageFormat"] = "mhd"  # not used because no result image written

        # Modify any other parameters indicated by kwargs here

        # Write the parameter text file
        import os

        saveFilePath = os.path.join(destDir, "ElastixParameters.txt")
        with open(saveFilePath, "w") as f:
            for key, val in p.items():
                # Convert to string if needed (TODO: what about hierarchies? handle arrays of values or handle string versions of these )
                if isinstance(val, str):
                    # Surround with quotes
                    valStr = '"%s"' % (val)
                else:
                    # Convert number to string (without quotes)
                    valStr = str(val)
                line = "(%s %s)\n" % (key, valStr)
                f.write(line)
        return saveFilePath

    def addLog(self, msg):
        """Print msg to python window; replaces similar fcn from Elastix.py module"""
        print(msg)


#
# PerfusionHelperTest
#


class PerfusionHelperTest(ScriptedLoadableModuleTest):
    """
    This is the test case for your scripted module.
    Uses ScriptedLoadableModuleTest base class, available at:
    https://github.com/Slicer/Slicer/blob/master/Base/Python/slicer/ScriptedLoadableModule.py
    """

    def setUp(self):
        """Do whatever is needed to reset the state - typically a scene clear will be enough."""
        slicer.mrmlScene.Clear()

    def runTest(self):
        """Run as few or as many tests as needed here."""
        self.setUp()
        self.test_PerfusionHelper1()

    def test_PerfusionHelper1(self):
        """Ideally you should have several levels of tests.  At the lowest level
        tests should exercise the functionality of the logic with different inputs
        (both valid and invalid).  At higher levels your tests should emulate the
        way the user would interact with your code and confirm that it still works
        the way you intended.
        One of the most important features of the tests is that it should alert other
        developers when their changes will have an impact on the behavior of your
        module.  For example, if a developer removes a feature that you depend on,
        your test should break so they know that the feature is needed.
        """

        self.delayDisplay("Starting the test")

        # Get/create input data

        import SampleData

        registerSampleData()
        inputVolume = SampleData.downloadSample("PerfusionHelper1")
        self.delayDisplay("Loaded test data set")

        inputScalarRange = inputVolume.GetImageData().GetScalarRange()
        self.assertEqual(inputScalarRange[0], 0)
        self.assertEqual(inputScalarRange[1], 695)

        outputVolume = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLScalarVolumeNode")
        threshold = 100

        # Test the module logic

        logic = PerfusionHelperLogic()

        # Test algorithm with non-inverted threshold
        logic.process(inputVolume, outputVolume, threshold, True)
        outputScalarRange = outputVolume.GetImageData().GetScalarRange()
        self.assertEqual(outputScalarRange[0], inputScalarRange[0])
        self.assertEqual(outputScalarRange[1], threshold)

        # Test algorithm with inverted threshold
        logic.process(inputVolume, outputVolume, threshold, False)
        outputScalarRange = outputVolume.GetImageData().GetScalarRange()
        self.assertEqual(outputScalarRange[0], inputScalarRange[0])
        self.assertEqual(outputScalarRange[1], inputScalarRange[1])

        self.delayDisplay("Test passed")
