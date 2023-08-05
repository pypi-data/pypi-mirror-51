# AUTO-GENERATED by tools/checkspecs.py - DO NOT EDIT
from __future__ import unicode_literals
from ..io import XNATSink


def test_XNATSink_inputs():
    input_map = dict(
        _outputs=dict(usedefault=True, ),
        assessor_id=dict(xor=['reconstruction_id'], ),
        cache_dir=dict(),
        config=dict(
            extensions=None,
            mandatory=True,
            xor=['server'],
        ),
        experiment_id=dict(mandatory=True, ),
        project_id=dict(mandatory=True, ),
        pwd=dict(),
        reconstruction_id=dict(xor=['assessor_id'], ),
        server=dict(
            mandatory=True,
            requires=['user', 'pwd'],
            xor=['config'],
        ),
        share=dict(usedefault=True, ),
        subject_id=dict(mandatory=True, ),
        user=dict(),
    )
    inputs = XNATSink.input_spec()

    for key, metadata in list(input_map.items()):
        for metakey, value in list(metadata.items()):
            assert getattr(inputs.traits()[key], metakey) == value
