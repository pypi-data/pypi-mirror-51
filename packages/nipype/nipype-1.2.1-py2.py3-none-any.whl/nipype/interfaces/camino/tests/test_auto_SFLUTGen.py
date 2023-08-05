# AUTO-GENERATED by tools/checkspecs.py - DO NOT EDIT
from __future__ import unicode_literals
from ..calib import SFLUTGen


def test_SFLUTGen_inputs():
    input_map = dict(
        args=dict(argstr='%s', ),
        binincsize=dict(
            argstr='-binincsize %d',
            units='NA',
        ),
        directmap=dict(argstr='-directmap', ),
        environ=dict(
            nohash=True,
            usedefault=True,
        ),
        in_file=dict(
            argstr='-inputfile %s',
            extensions=None,
            mandatory=True,
        ),
        info_file=dict(
            argstr='-infofile %s',
            extensions=None,
            mandatory=True,
        ),
        minvectsperbin=dict(
            argstr='-minvectsperbin %d',
            units='NA',
        ),
        order=dict(
            argstr='-order %d',
            units='NA',
        ),
        out_file=dict(
            argstr='> %s',
            genfile=True,
            position=-1,
        ),
        outputstem=dict(
            argstr='-outputstem %s',
            usedefault=True,
        ),
        pdf=dict(
            argstr='-pdf %s',
            usedefault=True,
        ),
    )
    inputs = SFLUTGen.input_spec()

    for key, metadata in list(input_map.items()):
        for metakey, value in list(metadata.items()):
            assert getattr(inputs.traits()[key], metakey) == value
def test_SFLUTGen_outputs():
    output_map = dict(
        lut_one_fibre=dict(extensions=None, ),
        lut_two_fibres=dict(extensions=None, ),
    )
    outputs = SFLUTGen.output_spec()

    for key, metadata in list(output_map.items()):
        for metakey, value in list(metadata.items()):
            assert getattr(outputs.traits()[key], metakey) == value
