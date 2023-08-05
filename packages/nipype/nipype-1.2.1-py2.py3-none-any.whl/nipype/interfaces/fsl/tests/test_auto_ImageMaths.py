# AUTO-GENERATED by tools/checkspecs.py - DO NOT EDIT
from __future__ import unicode_literals
from ..utils import ImageMaths


def test_ImageMaths_inputs():
    input_map = dict(
        args=dict(argstr='%s', ),
        environ=dict(
            nohash=True,
            usedefault=True,
        ),
        in_file=dict(
            argstr='%s',
            extensions=None,
            mandatory=True,
            position=1,
        ),
        in_file2=dict(
            argstr='%s',
            extensions=None,
            position=3,
        ),
        mask_file=dict(
            argstr='-mas %s',
            extensions=None,
        ),
        op_string=dict(
            argstr='%s',
            position=2,
        ),
        out_data_type=dict(
            argstr='-odt %s',
            position=-1,
        ),
        out_file=dict(
            argstr='%s',
            extensions=None,
            genfile=True,
            hash_files=False,
            position=-2,
        ),
        output_type=dict(),
        suffix=dict(),
    )
    inputs = ImageMaths.input_spec()

    for key, metadata in list(input_map.items()):
        for metakey, value in list(metadata.items()):
            assert getattr(inputs.traits()[key], metakey) == value
def test_ImageMaths_outputs():
    output_map = dict(out_file=dict(extensions=None, ), )
    outputs = ImageMaths.output_spec()

    for key, metadata in list(output_map.items()):
        for metakey, value in list(metadata.items()):
            assert getattr(outputs.traits()[key], metakey) == value
