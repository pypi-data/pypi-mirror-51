# AUTO-GENERATED by tools/checkspecs.py - DO NOT EDIT
from __future__ import unicode_literals
from ..preprocess import CALabel


def test_CALabel_inputs():
    input_map = dict(
        align=dict(argstr='-align', ),
        args=dict(argstr='%s', ),
        aseg=dict(argstr='-aseg %s', ),
        environ=dict(
            nohash=True,
            usedefault=True,
        ),
        in_file=dict(
            argstr='%s',
            extensions=None,
            mandatory=True,
            position=-4,
        ),
        in_vol=dict(
            argstr='-r %s',
            extensions=None,
        ),
        intensities=dict(
            argstr='-r %s',
            extensions=None,
        ),
        label=dict(argstr='-l %s', ),
        no_big_ventricles=dict(argstr='-nobigventricles', ),
        num_threads=dict(),
        out_file=dict(
            argstr='%s',
            extensions=None,
            mandatory=True,
            position=-1,
        ),
        prior=dict(argstr='-prior %.1f', ),
        relabel_unlikely=dict(argstr='-relabel_unlikely %d %.1f', ),
        subjects_dir=dict(),
        template=dict(
            argstr='%s',
            extensions=None,
            mandatory=True,
            position=-2,
        ),
        transform=dict(
            argstr='%s',
            extensions=None,
            mandatory=True,
            position=-3,
        ),
    )
    inputs = CALabel.input_spec()

    for key, metadata in list(input_map.items()):
        for metakey, value in list(metadata.items()):
            assert getattr(inputs.traits()[key], metakey) == value
def test_CALabel_outputs():
    output_map = dict(out_file=dict(extensions=None, ), )
    outputs = CALabel.output_spec()

    for key, metadata in list(output_map.items()):
        for metakey, value in list(metadata.items()):
            assert getattr(outputs.traits()[key], metakey) == value
