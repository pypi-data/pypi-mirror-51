# AUTO-GENERATED by tools/checkspecs.py - DO NOT EDIT
from __future__ import unicode_literals
from ..analysis import CoherenceAnalyzer


def test_CoherenceAnalyzer_inputs():
    input_map = dict(
        NFFT=dict(usedefault=True, ),
        TR=dict(),
        figure_type=dict(usedefault=True, ),
        frequency_range=dict(usedefault=True, ),
        in_TS=dict(),
        in_file=dict(
            extensions=None,
            requires=('TR', ),
        ),
        n_overlap=dict(usedefault=True, ),
        output_csv_file=dict(extensions=None, ),
        output_figure_file=dict(extensions=None, ),
    )
    inputs = CoherenceAnalyzer.input_spec()

    for key, metadata in list(input_map.items()):
        for metakey, value in list(metadata.items()):
            assert getattr(inputs.traits()[key], metakey) == value
def test_CoherenceAnalyzer_outputs():
    output_map = dict(
        coherence_array=dict(),
        coherence_csv=dict(extensions=None, ),
        coherence_fig=dict(extensions=None, ),
        timedelay_array=dict(),
        timedelay_csv=dict(extensions=None, ),
        timedelay_fig=dict(extensions=None, ),
    )
    outputs = CoherenceAnalyzer.output_spec()

    for key, metadata in list(output_map.items()):
        for metakey, value in list(metadata.items()):
            assert getattr(outputs.traits()[key], metakey) == value
