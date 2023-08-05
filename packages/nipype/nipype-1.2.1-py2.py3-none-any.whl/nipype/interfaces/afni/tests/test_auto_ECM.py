# AUTO-GENERATED by tools/checkspecs.py - DO NOT EDIT
from __future__ import unicode_literals
from ..preprocess import ECM


def test_ECM_inputs():
    input_map = dict(
        args=dict(argstr='%s', ),
        autoclip=dict(argstr='-autoclip', ),
        automask=dict(argstr='-automask', ),
        environ=dict(
            nohash=True,
            usedefault=True,
        ),
        eps=dict(argstr='-eps %f', ),
        fecm=dict(argstr='-fecm', ),
        full=dict(argstr='-full', ),
        in_file=dict(
            argstr='%s',
            copyfile=False,
            extensions=None,
            mandatory=True,
            position=-1,
        ),
        mask=dict(
            argstr='-mask %s',
            extensions=None,
        ),
        max_iter=dict(argstr='-max_iter %d', ),
        memory=dict(argstr='-memory %f', ),
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
        polort=dict(argstr='-polort %d', ),
        scale=dict(argstr='-scale %f', ),
        shift=dict(argstr='-shift %f', ),
        sparsity=dict(argstr='-sparsity %f', ),
        thresh=dict(argstr='-thresh %f', ),
    )
    inputs = ECM.input_spec()

    for key, metadata in list(input_map.items()):
        for metakey, value in list(metadata.items()):
            assert getattr(inputs.traits()[key], metakey) == value
def test_ECM_outputs():
    output_map = dict(out_file=dict(extensions=None, ), )
    outputs = ECM.output_spec()

    for key, metadata in list(output_map.items()):
        for metakey, value in list(metadata.items()):
            assert getattr(outputs.traits()[key], metakey) == value
