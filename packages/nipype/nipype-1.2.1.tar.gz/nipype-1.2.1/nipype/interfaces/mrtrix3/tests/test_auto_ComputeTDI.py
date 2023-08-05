# AUTO-GENERATED by tools/checkspecs.py - DO NOT EDIT
from __future__ import unicode_literals
from ..utils import ComputeTDI


def test_ComputeTDI_inputs():
    input_map = dict(
        args=dict(argstr='%s', ),
        contrast=dict(argstr='-constrast %s', ),
        data_type=dict(argstr='-datatype %s', ),
        dixel=dict(
            argstr='-dixel %s',
            extensions=None,
        ),
        ends_only=dict(argstr='-ends_only', ),
        environ=dict(
            nohash=True,
            usedefault=True,
        ),
        fwhm_tck=dict(argstr='-fwhm_tck %f', ),
        in_file=dict(
            argstr='%s',
            extensions=None,
            mandatory=True,
            position=-2,
        ),
        in_map=dict(
            argstr='-image %s',
            extensions=None,
        ),
        map_zero=dict(argstr='-map_zero', ),
        max_tod=dict(argstr='-tod %d', ),
        nthreads=dict(
            argstr='-nthreads %d',
            nohash=True,
        ),
        out_file=dict(
            argstr='%s',
            extensions=None,
            position=-1,
            usedefault=True,
        ),
        precise=dict(argstr='-precise', ),
        reference=dict(
            argstr='-template %s',
            extensions=None,
        ),
        stat_tck=dict(argstr='-stat_tck %s', ),
        stat_vox=dict(argstr='-stat_vox %s', ),
        tck_weights=dict(
            argstr='-tck_weights_in %s',
            extensions=None,
        ),
        upsample=dict(argstr='-upsample %d', ),
        use_dec=dict(argstr='-dec', ),
        vox_size=dict(
            argstr='-vox %s',
            sep=',',
        ),
    )
    inputs = ComputeTDI.input_spec()

    for key, metadata in list(input_map.items()):
        for metakey, value in list(metadata.items()):
            assert getattr(inputs.traits()[key], metakey) == value
def test_ComputeTDI_outputs():
    output_map = dict(out_file=dict(extensions=None, ), )
    outputs = ComputeTDI.output_spec()

    for key, metadata in list(output_map.items()):
        for metakey, value in list(metadata.items()):
            assert getattr(outputs.traits()[key], metakey) == value
