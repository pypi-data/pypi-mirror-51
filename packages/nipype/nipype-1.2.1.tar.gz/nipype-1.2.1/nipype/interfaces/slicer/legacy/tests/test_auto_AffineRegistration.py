# AUTO-GENERATED by tools/checkspecs.py - DO NOT EDIT
from __future__ import unicode_literals
from ..registration import AffineRegistration


def test_AffineRegistration_inputs():
    input_map = dict(
        FixedImageFileName=dict(
            argstr='%s',
            extensions=None,
            position=-2,
        ),
        MovingImageFileName=dict(
            argstr='%s',
            extensions=None,
            position=-1,
        ),
        args=dict(argstr='%s', ),
        environ=dict(
            nohash=True,
            usedefault=True,
        ),
        fixedsmoothingfactor=dict(argstr='--fixedsmoothingfactor %d', ),
        histogrambins=dict(argstr='--histogrambins %d', ),
        initialtransform=dict(
            argstr='--initialtransform %s',
            extensions=None,
        ),
        iterations=dict(argstr='--iterations %d', ),
        movingsmoothingfactor=dict(argstr='--movingsmoothingfactor %d', ),
        outputtransform=dict(
            argstr='--outputtransform %s',
            hash_files=False,
        ),
        resampledmovingfilename=dict(
            argstr='--resampledmovingfilename %s',
            hash_files=False,
        ),
        spatialsamples=dict(argstr='--spatialsamples %d', ),
        translationscale=dict(argstr='--translationscale %f', ),
    )
    inputs = AffineRegistration.input_spec()

    for key, metadata in list(input_map.items()):
        for metakey, value in list(metadata.items()):
            assert getattr(inputs.traits()[key], metakey) == value
def test_AffineRegistration_outputs():
    output_map = dict(
        outputtransform=dict(extensions=None, ),
        resampledmovingfilename=dict(extensions=None, ),
    )
    outputs = AffineRegistration.output_spec()

    for key, metadata in list(output_map.items()):
        for metakey, value in list(metadata.items()):
            assert getattr(outputs.traits()[key], metakey) == value
