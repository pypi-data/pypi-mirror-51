# AUTO-GENERATED by tools/checkspecs.py - DO NOT EDIT
from __future__ import unicode_literals
from ..preprocess import BlurToFWHM


def test_BlurToFWHM_inputs():
    input_map = dict(
        args=dict(argstr='%s', ),
        automask=dict(argstr='-automask', ),
        blurmaster=dict(
            argstr='-blurmaster %s',
            extensions=None,
        ),
        environ=dict(
            nohash=True,
            usedefault=True,
        ),
        fwhm=dict(argstr='-FWHM %f', ),
        fwhmxy=dict(argstr='-FWHMxy %f', ),
        in_file=dict(
            argstr='-input %s',
            extensions=None,
            mandatory=True,
        ),
        mask=dict(
            argstr='-mask %s',
            extensions=None,
        ),
        num_threads=dict(
            nohash=True,
            usedefault=True,
        ),
        out_file=dict(
            argstr='-prefix %s',
            extensions=None,
            name_source=['in_file'],
            name_template='%s_afni',
        ),
        outputtype=dict(),
    )
    inputs = BlurToFWHM.input_spec()

    for key, metadata in list(input_map.items()):
        for metakey, value in list(metadata.items()):
            assert getattr(inputs.traits()[key], metakey) == value
def test_BlurToFWHM_outputs():
    output_map = dict(out_file=dict(extensions=None, ), )
    outputs = BlurToFWHM.output_spec()

    for key, metadata in list(output_map.items()):
        for metakey, value in list(metadata.items()):
            assert getattr(outputs.traits()[key], metakey) == value
