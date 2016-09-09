# Auto generated configuration file
# using: 
# Revision: 1.19 
# Source: /local/reps/CMSSW/CMSSW/Configuration/Applications/python/ConfigBuilder.py,v 
# with command line options: Hadronizer_TuneCUETP8M1_13TeV_generic_LHE_pythia8_cff.py --fileout file:EXO-RunIISummer15GS-01246.root --customise SLHCUpgradeSimulations/Configuration/postLS1Customs.customisePostLS1,Configuration/DataProcessing/Utils.addMonitoring --step GEN --conditions auto:mc --datatier GEN-SIM --eventcontent RAWSIM -n 1 --filein=file:tt-4p-600-1100-v1510_14TEV_183994371.lhe --no_exec
import FWCore.ParameterSet.Config as cms

process = cms.Process('GEN')

from FWCore.ParameterSet.VarParsing import VarParsing
options = VarParsing ('python')

options.register('skipEvents',
                 0,
                 VarParsing.multiplicity.singleton,
                 VarParsing.varType.int,
                 "Skip events before processing")

#options.setDefault('maxEvents', 20000)
options.parseArguments()
#maxEvt = options.maxEvents
maxEvt = 20000
inFiles = options.inputFiles #='file:/uscms_data/d3/easmith/DelphesThings/TheirDelphes/LHEFiles/WbT_leftHanded_M1_events.lhe']
outFile = options.outputFile# = 'genout.root'
#outFile = 'genout.root'
#inFiles = ['file:/uscms_data/d3/easmith/DelphesThings/TheirDelphes/LHEFiles/WbT_leftHanded_M1_events.lhe']
skipEvt = options.skipEvents
print options

# import of standard configurations
process.load('Configuration.StandardSequences.Services_cff')
process.load('SimGeneral.HepPDTESSource.pythiapdt_cfi')
process.load('FWCore.MessageService.MessageLogger_cfi')
process.load('Configuration.EventContent.EventContent_cff')
process.load('SimGeneral.MixingModule.mixNoPU_cfi')
process.load('Configuration.StandardSequences.GeometryRecoDB_cff')
process.load('Configuration.StandardSequences.MagneticField_38T_cff')
process.load('Configuration.StandardSequences.Generator_cff')
process.load('IOMC.EventVertexGenerators.VtxSmearedRealistic8TeVCollision_cfi')
process.load('GeneratorInterface.Core.genFilterSummary_cff')
process.load('Configuration.StandardSequences.EndOfProcess_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_condDBv2_cff')

###SJ
from Configuration.Generator.Pythia8CommonSettings_cfi import *
from Configuration.Generator.Pythia8CUEP8M1Settings_cfi import *
###SJ
process.MessageLogger.cerr.FwkReport.reportEvery = 1000
process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(maxEvt) #run on 20k events
)

# Input source
process.source = cms.Source("LHESource",
			    skipEvents=cms.untracked.uint32(skipEvt), 
                            fileNames = cms.untracked.vstring( inFiles )
			  
)
print process.source
process.options = cms.untracked.PSet(

)

# Production Info
process.configurationMetadata = cms.untracked.PSet(
    version = cms.untracked.string('$Revision: 1.19 $'),
    annotation = cms.untracked.string('Hadronizer_TuneCUETP8M1_13TeV_generic_LHE_pythia8_cff.py nevts:1'),
    name = cms.untracked.string('Applications')
)

# Output definition

process.RAWSIMoutput = cms.OutputModule("PoolOutputModule",
    splitLevel = cms.untracked.int32(0),
    eventAutoFlushCompressedSize = cms.untracked.int32(5242880),
    outputCommands = process.RAWSIMEventContent.outputCommands,
    fileName = cms.untracked.string('file:'+outFile),
    dataset = cms.untracked.PSet(
                filterName = cms.untracked.string(''),
                dataTier = cms.untracked.string('GEN-SIM')
                ),
    SelectEvents = cms.untracked.PSet(
                SelectEvents = cms.vstring('generation_step')
                )
)
print process.RAWSIMoutput.fileName

# Additional output definition
#*********************************************************************
# Matching - Warning! ickkw > 1 is still beta
#*********************************************************************
# 1        = ickkw            ! 0 no matching, 1 MLM, 2 CKKW matching
#*********************************************************************
#*********************************************************************
# maximal pdg code for quark to be considered as a light jet         *
# (otherwise b cuts are applied)                                     *
#*********************************************************************
# 5 = maxjetflavor    ! Maximum jet pdg code
#*********************************************************************
# Jet measure cuts                                                   *
#*********************************************************************
# 40   = xqcut   ! minimum kt jet measure between partons
#*********************************************************************

# Other statements
process.genstepfilter.triggerConditions=cms.vstring("generation_step")
from Configuration.AlCa.GlobalTag_condDBv2 import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, 'auto:mc', '')

process.generator = cms.EDFilter("Pythia8HadronizerFilter",
    pythiaPylistVerbosity = cms.untracked.int32(1),
    filterEfficiency = cms.untracked.double(1.0),
    pythiaHepMCVerbosity = cms.untracked.bool(False),
    comEnergy = cms.double(14000.0),
    maxEventsToPrint = cms.untracked.int32(1),
    PythiaParameters = cms.PSet(
		pythia8CommonSettingsBlock,  ###SJ
		pythia8CUEP8M1SettingsBlock,   ###SJ
		parameterSets = cms.vstring('pythia8CommonSettings', 
					    'pythia8CUEP8M1Settings',
					    )
                )                                 
)#close EDFilter

process.ProductionFilterSequence = cms.Sequence(process.generator)

# Path and EndPath definitions
process.generation_step = cms.Path(process.pgen)
process.genfiltersummary_step = cms.EndPath(process.genFilterSummary)
process.endjob_step = cms.EndPath(process.endOfProcess)
process.RAWSIMoutput_step = cms.EndPath(process.RAWSIMoutput)

# Schedule definition
process.schedule = cms.Schedule(process.generation_step,process.genfiltersummary_step,process.endjob_step,process.RAWSIMoutput_step)
# filter all path with the production filter sequence
for path in process.paths:
	getattr(process,path)._seq = process.ProductionFilterSequence * getattr(process,path)._seq 

# customisation of the process.

# Automatic addition of the customisation function from SLHCUpgradeSimulations.Configuration.postLS1Customs
from SLHCUpgradeSimulations.Configuration.postLS1Customs import customisePostLS1 

#call to customisation function customisePostLS1 imported from SLHCUpgradeSimulations.Configuration.postLS1Customs
process = customisePostLS1(process)

# Automatic addition of the customisation function from Configuration.DataProcessing.Utils
from Configuration.DataProcessing.Utils import addMonitoring 

#call to customisation function addMonitoring imported from Configuration.DataProcessing.Utils
process = addMonitoring(process)

# End of customisation functions
