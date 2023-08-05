# AUTO-GENERATED by tools/checkspecs.py - DO NOT EDIT
from __future__ import unicode_literals
from ..preprocess import OutlierCount


def test_OutlierCount_inputs():
    input_map = dict(
        args=dict(argstr='%s', ),
        autoclip=dict(
            argstr='-autoclip',
            usedefault=True,
            xor=['mask'],
        ),
        automask=dict(
            argstr='-automask',
            usedefault=True,
            xor=['mask'],
        ),
        environ=dict(
            nohash=True,
            usedefault=True,
        ),
        fraction=dict(
            argstr='-fraction',
            usedefault=True,
        ),
        in_file=dict(
            argstr='%s',
            extensions=None,
            mandatory=True,
            position=-2,
        ),
        interval=dict(
            argstr='-range',
            usedefault=True,
        ),
        legendre=dict(
            argstr='-legendre',
            usedefault=True,
        ),
        mask=dict(
            argstr='-mask %s',
            extensions=None,
            xor=['autoclip', 'automask'],
        ),
        out_file=dict(
            extensions=None,
            keep_extension=False,
            name_source=['in_file'],
            name_template='%s_outliers',
        ),
        outliers_file=dict(
            argstr='-save %s',
            extensions=None,
            keep_extension=True,
            name_source=['in_file'],
            name_template='%s_outliers',
            output_name='out_outliers',
        ),
        polort=dict(argstr='-polort %d', ),
        qthr=dict(
            argstr='-qthr %.5f',
            usedefault=True,
        ),
        save_outliers=dict(usedefault=True, ),
    )
    inputs = OutlierCount.input_spec()

    for key, metadata in list(input_map.items()):
        for metakey, value in list(metadata.items()):
            assert getattr(inputs.traits()[key], metakey) == value
def test_OutlierCount_outputs():
    output_map = dict(
        out_file=dict(extensions=None, ),
        out_outliers=dict(extensions=None, ),
    )
    outputs = OutlierCount.output_spec()

    for key, metadata in list(output_map.items()):
        for metakey, value in list(metadata.items()):
            assert getattr(outputs.traits()[key], metakey) == value
