# AUTO-GENERATED by tools/checkspecs.py - DO NOT EDIT
from __future__ import unicode_literals
from ..registration import affScalarVolTask


def test_affScalarVolTask_inputs():
    input_map = dict(
        args=dict(argstr='%s', ),
        deformation=dict(
            argstr='-deformation %g %g %g %g %g %g',
            xor=['transform'],
        ),
        environ=dict(
            nohash=True,
            usedefault=True,
        ),
        euler=dict(
            argstr='-euler %g %g %g',
            xor=['transform'],
        ),
        in_file=dict(
            argstr='-in %s',
            extensions=None,
            mandatory=True,
        ),
        interpolation=dict(
            argstr='-interp %s',
            usedefault=True,
        ),
        out_file=dict(
            argstr='-out %s',
            extensions=None,
            keep_extension=True,
            name_source='in_file',
            name_template='%s_affxfmd',
        ),
        target=dict(
            argstr='-target %s',
            extensions=None,
            xor=['transform'],
        ),
        transform=dict(
            argstr='-trans %s',
            extensions=None,
            xor=['target', 'translation', 'euler', 'deformation'],
        ),
        translation=dict(
            argstr='-translation %g %g %g',
            xor=['transform'],
        ),
    )
    inputs = affScalarVolTask.input_spec()

    for key, metadata in list(input_map.items()):
        for metakey, value in list(metadata.items()):
            assert getattr(inputs.traits()[key], metakey) == value
def test_affScalarVolTask_outputs():
    output_map = dict(out_file=dict(extensions=None, ), )
    outputs = affScalarVolTask.output_spec()

    for key, metadata in list(output_map.items()):
        for metakey, value in list(metadata.items()):
            assert getattr(outputs.traits()[key], metakey) == value
