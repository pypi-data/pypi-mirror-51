# AUTO-GENERATED by tools/checkspecs.py - DO NOT EDIT
from __future__ import unicode_literals
from ..preprocess import WatershedSkullStrip


def test_WatershedSkullStrip_inputs():
    input_map = dict(
        args=dict(argstr='%s', ),
        brain_atlas=dict(
            argstr='-brain_atlas %s',
            extensions=None,
            position=-4,
        ),
        environ=dict(
            nohash=True,
            usedefault=True,
        ),
        in_file=dict(
            argstr='%s',
            extensions=None,
            mandatory=True,
            position=-2,
        ),
        out_file=dict(
            argstr='%s',
            extensions=None,
            mandatory=True,
            position=-1,
            usedefault=True,
        ),
        subjects_dir=dict(),
        t1=dict(argstr='-T1', ),
        transform=dict(
            argstr='%s',
            extensions=None,
            position=-3,
        ),
    )
    inputs = WatershedSkullStrip.input_spec()

    for key, metadata in list(input_map.items()):
        for metakey, value in list(metadata.items()):
            assert getattr(inputs.traits()[key], metakey) == value
def test_WatershedSkullStrip_outputs():
    output_map = dict(out_file=dict(extensions=None, ), )
    outputs = WatershedSkullStrip.output_spec()

    for key, metadata in list(output_map.items()):
        for metakey, value in list(metadata.items()):
            assert getattr(outputs.traits()[key], metakey) == value
