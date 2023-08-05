# AUTO-GENERATED by tools/checkspecs.py - DO NOT EDIT
from __future__ import unicode_literals
from ..ukftractography import UKFTractography


def test_UKFTractography_inputs():
    input_map = dict(
        Ql=dict(argstr='--Ql %f', ),
        Qm=dict(argstr='--Qm %f', ),
        Qw=dict(argstr='--Qw %f', ),
        Rs=dict(argstr='--Rs %f', ),
        args=dict(argstr='%s', ),
        dwiFile=dict(
            argstr='--dwiFile %s',
            extensions=None,
        ),
        environ=dict(
            nohash=True,
            usedefault=True,
        ),
        freeWater=dict(argstr='--freeWater ', ),
        fullTensorModel=dict(argstr='--fullTensorModel ', ),
        labels=dict(
            argstr='--labels %s',
            sep=',',
        ),
        maskFile=dict(
            argstr='--maskFile %s',
            extensions=None,
        ),
        maxBranchingAngle=dict(argstr='--maxBranchingAngle %f', ),
        maxHalfFiberLength=dict(argstr='--maxHalfFiberLength %f', ),
        minBranchingAngle=dict(argstr='--minBranchingAngle %f', ),
        minFA=dict(argstr='--minFA %f', ),
        minGA=dict(argstr='--minGA %f', ),
        numTensor=dict(argstr='--numTensor %s', ),
        numThreads=dict(argstr='--numThreads %d', ),
        recordCovariance=dict(argstr='--recordCovariance ', ),
        recordFA=dict(argstr='--recordFA ', ),
        recordFreeWater=dict(argstr='--recordFreeWater ', ),
        recordLength=dict(argstr='--recordLength %f', ),
        recordNMSE=dict(argstr='--recordNMSE ', ),
        recordState=dict(argstr='--recordState ', ),
        recordTensors=dict(argstr='--recordTensors ', ),
        recordTrace=dict(argstr='--recordTrace ', ),
        seedFALimit=dict(argstr='--seedFALimit %f', ),
        seedsFile=dict(
            argstr='--seedsFile %s',
            extensions=None,
        ),
        seedsPerVoxel=dict(argstr='--seedsPerVoxel %d', ),
        stepLength=dict(argstr='--stepLength %f', ),
        storeGlyphs=dict(argstr='--storeGlyphs ', ),
        tracts=dict(
            argstr='--tracts %s',
            hash_files=False,
        ),
        tractsWithSecondTensor=dict(
            argstr='--tractsWithSecondTensor %s',
            hash_files=False,
        ),
        writeAsciiTracts=dict(argstr='--writeAsciiTracts ', ),
        writeUncompressedTracts=dict(argstr='--writeUncompressedTracts ', ),
    )
    inputs = UKFTractography.input_spec()

    for key, metadata in list(input_map.items()):
        for metakey, value in list(metadata.items()):
            assert getattr(inputs.traits()[key], metakey) == value
def test_UKFTractography_outputs():
    output_map = dict(
        tracts=dict(extensions=None, ),
        tractsWithSecondTensor=dict(extensions=None, ),
    )
    outputs = UKFTractography.output_spec()

    for key, metadata in list(output_map.items()):
        for metakey, value in list(metadata.items()):
            assert getattr(outputs.traits()[key], metakey) == value
