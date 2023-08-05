# AUTO-GENERATED by tools/checkspecs.py - DO NOT EDIT
from __future__ import unicode_literals
from ..preprocess import TShift


def test_TShift_inputs():
    input_map = dict(
        args=dict(argstr='%s', ),
        environ=dict(
            nohash=True,
            usedefault=True,
        ),
        ignore=dict(argstr='-ignore %s', ),
        in_file=dict(
            argstr='%s',
            copyfile=False,
            extensions=None,
            mandatory=True,
            position=-1,
        ),
        interp=dict(argstr='-%s', ),
        num_threads=dict(
            nohash=True,
            usedefault=True,
        ),
        out_file=dict(
            argstr='-prefix %s',
            extensions=None,
            name_source='in_file',
            name_template='%s_tshift',
        ),
        outputtype=dict(),
        rlt=dict(argstr='-rlt', ),
        rltplus=dict(argstr='-rlt+', ),
        slice_encoding_direction=dict(usedefault=True, ),
        slice_timing=dict(
            argstr='-tpattern @%s',
            xor=['tpattern'],
        ),
        tpattern=dict(
            argstr='-tpattern %s',
            xor=['slice_timing'],
        ),
        tr=dict(argstr='-TR %s', ),
        tslice=dict(
            argstr='-slice %s',
            xor=['tzero'],
        ),
        tzero=dict(
            argstr='-tzero %s',
            xor=['tslice'],
        ),
    )
    inputs = TShift.input_spec()

    for key, metadata in list(input_map.items()):
        for metakey, value in list(metadata.items()):
            assert getattr(inputs.traits()[key], metakey) == value
def test_TShift_outputs():
    output_map = dict(
        out_file=dict(extensions=None, ),
        timing_file=dict(extensions=None, ),
    )
    outputs = TShift.output_spec()

    for key, metadata in list(output_map.items()):
        for metakey, value in list(metadata.items()):
            assert getattr(outputs.traits()[key], metakey) == value
