# AUTO-GENERATED by tools/checkspecs.py - DO NOT EDIT
from __future__ import unicode_literals
from ..preprocess import DARTELNorm2MNI


def test_DARTELNorm2MNI_inputs():
    input_map = dict(
        apply_to_files=dict(
            copyfile=False,
            field='mni_norm.data.subjs.images',
            mandatory=True,
        ),
        bounding_box=dict(field='mni_norm.bb', ),
        flowfield_files=dict(
            field='mni_norm.data.subjs.flowfields',
            mandatory=True,
        ),
        fwhm=dict(field='mni_norm.fwhm', ),
        matlab_cmd=dict(),
        mfile=dict(usedefault=True, ),
        modulate=dict(field='mni_norm.preserve', ),
        paths=dict(),
        template_file=dict(
            copyfile=False,
            extensions=['.hdr', '.img', '.img.gz', '.nii'],
            field='mni_norm.template',
            mandatory=True,
        ),
        use_mcr=dict(),
        use_v8struct=dict(
            min_ver='8',
            usedefault=True,
        ),
        voxel_size=dict(field='mni_norm.vox', ),
    )
    inputs = DARTELNorm2MNI.input_spec()

    for key, metadata in list(input_map.items()):
        for metakey, value in list(metadata.items()):
            assert getattr(inputs.traits()[key], metakey) == value
def test_DARTELNorm2MNI_outputs():
    output_map = dict(
        normalization_parameter_file=dict(extensions=None, ),
        normalized_files=dict(),
    )
    outputs = DARTELNorm2MNI.output_spec()

    for key, metadata in list(output_map.items()):
        for metakey, value in list(metadata.items()):
            assert getattr(outputs.traits()[key], metakey) == value
