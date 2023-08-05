# AUTO-GENERATED by tools/checkspecs.py - DO NOT EDIT
from __future__ import unicode_literals
from ..maths import Merge


def test_Merge_inputs():
    input_map = dict(
        args=dict(argstr='%s', ),
        dimension=dict(mandatory=True, ),
        environ=dict(
            nohash=True,
            usedefault=True,
        ),
        in_file=dict(
            argstr='%s',
            extensions=None,
            mandatory=True,
            position=2,
        ),
        merge_files=dict(
            argstr='%s',
            mandatory=True,
            position=4,
        ),
        out_file=dict(
            argstr='%s',
            extensions=None,
            name_source=['in_file'],
            name_template='%s',
            position=-2,
        ),
        output_datatype=dict(
            argstr='-odt %s',
            position=-3,
        ),
    )
    inputs = Merge.input_spec()

    for key, metadata in list(input_map.items()):
        for metakey, value in list(metadata.items()):
            assert getattr(inputs.traits()[key], metakey) == value
def test_Merge_outputs():
    output_map = dict(out_file=dict(extensions=None, ), )
    outputs = Merge.output_spec()

    for key, metadata in list(output_map.items()):
        for metakey, value in list(metadata.items()):
            assert getattr(outputs.traits()[key], metakey) == value
