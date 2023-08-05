# AUTO-GENERATED by tools/checkspecs.py - DO NOT EDIT
from __future__ import unicode_literals
from ..c3 import C3d


def test_C3d_inputs():
    input_map = dict(
        args=dict(argstr='%s', ),
        environ=dict(
            nohash=True,
            usedefault=True,
        ),
        in_file=dict(
            argstr='%s',
            mandatory=True,
            position=1,
        ),
        interp=dict(argstr='-interpolation %s', ),
        is_4d=dict(usedefault=True, ),
        multicomp_split=dict(
            argstr='-mcr',
            position=0,
            usedefault=True,
        ),
        out_file=dict(
            argstr='-o %s',
            extensions=None,
            position=-1,
            xor=['out_files'],
        ),
        out_files=dict(
            argstr='-oo %s',
            position=-1,
            xor=['out_file'],
        ),
        pix_type=dict(argstr='-type %s', ),
        resample=dict(argstr='-resample %s', ),
        scale=dict(argstr='-scale %s', ),
        shift=dict(argstr='-shift %s', ),
        smooth=dict(argstr='-smooth %s', ),
    )
    inputs = C3d.input_spec()

    for key, metadata in list(input_map.items()):
        for metakey, value in list(metadata.items()):
            assert getattr(inputs.traits()[key], metakey) == value
def test_C3d_outputs():
    output_map = dict(out_files=dict(), )
    outputs = C3d.output_spec()

    for key, metadata in list(output_map.items()):
        for metakey, value in list(metadata.items()):
            assert getattr(outputs.traits()[key], metakey) == value
