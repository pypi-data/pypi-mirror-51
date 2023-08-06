"""Biologically-related useful methods."""

from .biotools import (
    blast_sequence,
    change_biopython_record_sequence,
    complement,
    dna_pattern_to_regexpr,
    find_specification_in_feature,
    gc_content,
    group_nearby_indices,
    group_nearby_segments,
    is_palyndromic,
    list_common_enzymes,
    load_record,
    random_dna_sequence,
    random_protein_sequence,
    reverse_complement,
    reverse_translate,
    sequences_differences,
    sequences_differences_array,
    sequences_differences_segments,
    sequence_to_biopython_record,
    subdivide_window,
    translate,
    windows_overlap,
    codons_frequencies_and_positions,
    dict_to_pretty_string
)

from .features_annotations import (
    annotate_record,
    annotate_differences,
    annotate_pattern_occurrences
)

from .biotables import (CODONS_SEQUENCES, CODONS_TRANSLATIONS, IUPAC_NOTATION,
                        NUCLEOTIDE_TO_REGEXPR)
