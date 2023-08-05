# AUTO-GENERATED by tools/checkspecs.py - DO NOT EDIT
from __future__ import unicode_literals
from ..connectivity import LabelConvert


def test_LabelConvert_inputs():
    input_map = dict(
        args=dict(argstr='%s', ),
        environ=dict(
            nohash=True,
            usedefault=True,
        ),
        in_config=dict(
            argstr='%s',
            extensions=None,
            position=-2,
        ),
        in_file=dict(
            argstr='%s',
            extensions=None,
            mandatory=True,
            position=-4,
        ),
        in_lut=dict(
            argstr='%s',
            extensions=None,
            mandatory=True,
            position=-3,
        ),
        num_threads=dict(
            argstr='-nthreads %d',
            nohash=True,
        ),
        out_file=dict(
            argstr='%s',
            extensions=None,
            mandatory=True,
            position=-1,
            usedefault=True,
        ),
        spine=dict(
            argstr='-spine %s',
            extensions=None,
        ),
    )
    inputs = LabelConvert.input_spec()

    for key, metadata in list(input_map.items()):
        for metakey, value in list(metadata.items()):
            assert getattr(inputs.traits()[key], metakey) == value
def test_LabelConvert_outputs():
    output_map = dict(out_file=dict(extensions=None, ), )
    outputs = LabelConvert.output_spec()

    for key, metadata in list(output_map.items()):
        for metakey, value in list(metadata.items()):
            assert getattr(outputs.traits()[key], metakey) == value
