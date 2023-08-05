# AUTO-GENERATED by tools/checkspecs.py - DO NOT EDIT
from __future__ import unicode_literals
from ..resampling import ApplyTransforms


def test_ApplyTransforms_inputs():
    input_map = dict(
        args=dict(argstr='%s', ),
        default_value=dict(
            argstr='--default-value %g',
            usedefault=True,
        ),
        dimension=dict(argstr='--dimensionality %d', ),
        environ=dict(
            nohash=True,
            usedefault=True,
        ),
        float=dict(
            argstr='--float %d',
            usedefault=True,
        ),
        input_image=dict(
            argstr='--input %s',
            extensions=None,
            mandatory=True,
        ),
        input_image_type=dict(argstr='--input-image-type %d', ),
        interpolation=dict(
            argstr='%s',
            usedefault=True,
        ),
        interpolation_parameters=dict(),
        invert_transform_flags=dict(),
        num_threads=dict(
            nohash=True,
            usedefault=True,
        ),
        out_postfix=dict(usedefault=True, ),
        output_image=dict(
            argstr='--output %s',
            genfile=True,
            hash_files=False,
        ),
        print_out_composite_warp_file=dict(requires=['output_image'], ),
        reference_image=dict(
            argstr='--reference-image %s',
            extensions=None,
            mandatory=True,
        ),
        transforms=dict(
            argstr='%s',
            mandatory=True,
        ),
    )
    inputs = ApplyTransforms.input_spec()

    for key, metadata in list(input_map.items()):
        for metakey, value in list(metadata.items()):
            assert getattr(inputs.traits()[key], metakey) == value
def test_ApplyTransforms_outputs():
    output_map = dict(output_image=dict(extensions=None, ), )
    outputs = ApplyTransforms.output_spec()

    for key, metadata in list(output_map.items()):
        for metakey, value in list(metadata.items()):
            assert getattr(outputs.traits()[key], metakey) == value
