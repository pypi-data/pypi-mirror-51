# AUTO-GENERATED by tools/checkspecs.py - DO NOT EDIT
from __future__ import unicode_literals
from ..utils import AffineInitializer


def test_AffineInitializer_inputs():
    input_map = dict(
        args=dict(argstr='%s', ),
        dimension=dict(
            argstr='%s',
            position=0,
            usedefault=True,
        ),
        environ=dict(
            nohash=True,
            usedefault=True,
        ),
        fixed_image=dict(
            argstr='%s',
            extensions=None,
            mandatory=True,
            position=1,
        ),
        local_search=dict(
            argstr='%d',
            position=7,
            usedefault=True,
        ),
        moving_image=dict(
            argstr='%s',
            extensions=None,
            mandatory=True,
            position=2,
        ),
        num_threads=dict(
            nohash=True,
            usedefault=True,
        ),
        out_file=dict(
            argstr='%s',
            extensions=None,
            position=3,
            usedefault=True,
        ),
        principal_axes=dict(
            argstr='%d',
            position=6,
            usedefault=True,
        ),
        radian_fraction=dict(
            argstr='%f',
            position=5,
            usedefault=True,
        ),
        search_factor=dict(
            argstr='%f',
            position=4,
            usedefault=True,
        ),
    )
    inputs = AffineInitializer.input_spec()

    for key, metadata in list(input_map.items()):
        for metakey, value in list(metadata.items()):
            assert getattr(inputs.traits()[key], metakey) == value
def test_AffineInitializer_outputs():
    output_map = dict(out_file=dict(extensions=None, ), )
    outputs = AffineInitializer.output_spec()

    for key, metadata in list(output_map.items()):
        for metakey, value in list(metadata.items()):
            assert getattr(outputs.traits()[key], metakey) == value
