# -*- coding: utf-8 -*-

"""
test_refchooser
----------------------------------

Tests for `refchooser` module.
"""

from Bio import SeqIO
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord
import os
import random
import re

from refchooser import refchooser
from refchooser import utils


def make_random_dna_string(length, allowed_bases):
    """Create random DNA sequence string of the specified length.
    Parameters
    ----------
    length : int
        The length of the DNA string being generated.
    allowed_bases : str
        A string of possible bases.
    Returns
    -------
    str
        Random DNA string
    """
    char_list = [random.choice(allowed_bases) for _ in range(length)]
    return "".join(char_list)


def write_fasta(seq_strings, directory, file_name, defline_prefix=""):
    """Write sequences to a fasta file.

    Parameters
    ----------
    seq_strings : list of str
        Sequences of nucleotide characters to write to the fasta file
    directory : str
        Directory of the fasta file to write
    file_name : str
        File name of the fasta file to write
    defline_prefix : str, optional
        Prefix prepended to id, name, description.  Defaults to "".

    Returns
    -------
    str
        Path of fasta file
    """
    records = []
    for i, seq_string in enumerate(seq_strings):
        seq_num_str = defline_prefix + str(1 + i)
        ident = "Id" + seq_num_str
        name = "Name" + seq_num_str
        description = "Description" + seq_num_str
        seq = Seq(seq_string)
        record = SeqRecord(seq, ident, name, description)
        records.append(record)

    file_path = os.path.join(directory, file_name)
    SeqIO.write(records, file_path, "fasta")
    return file_path


def write_random_dna_fasta(directory, file_name, length, allowed_bases="GATC"):
    """Write a random dna string of a specified length to a temporary fasta file.
    The fasta file will also contain a random ID, name, and description.

    Parameters
    ----------
    directory : str
        Directory of the fasta file to write
    file_name : str
        File name of the fasta file to write
    length : int
        Length of nucleotide sequence generate and write to the fasta file
    allowed_bases : str, optional
        A string of possible bases.  Defaults to 'GATC'

    Returns
    -------
    file_path : str
        Path of fasta file
    dna : str
        Generated DNA string
    """
    dna = make_random_dna_string(length, allowed_bases)
    file_path = write_fasta([dna], directory, file_name)
    return (file_path, dna)


def test_sketch(tmpdir):
    """Verify sketches are created."""
    fasta_dir = str(tmpdir.mkdir("fastadir"))
    sketch_dir = str(tmpdir.mkdir("sketchdir"))
    path1, _ = write_random_dna_fasta(fasta_dir, "fasta1.fasta", 10000)
    path2, _ = write_random_dna_fasta(fasta_dir, "fasta2.fasta", 10000)
    refchooser.sketch(fasta_dir, sketch_dir, 1000)
    sketches = os.listdir(sketch_dir)
    assert "fasta1.msh" in sketches
    assert "fasta2.msh" in sketches


def test_get_distance_matrix(tmpdir, capsys):
    """Verify correct distance matrix."""
    fasta_dir = str(tmpdir.mkdir("fastadir"))
    sketch_dir = str(tmpdir.mkdir("sketchdir"))
    dna1 = 'A' * 100
    dna2 = 'C' * 100
    write_fasta([dna1], fasta_dir, "fasta1.fasta")
    write_fasta([dna2], fasta_dir, "fasta2.fasta")
    fasta_paths = utils.get_file_list(fasta_dir)
    sketch_size = 1000
    df = refchooser.get_distance_matrix(fasta_paths, sketch_dir, sketch_size)
    assert df.loc["fasta1", "fasta1"] == 0
    assert df.loc["fasta1", "fasta2"] == 1
    assert df.loc["fasta2", "fasta1"] == 1
    assert df.loc["fasta2", "fasta2"] == 0


def test_distance_matrix(tmpdir, capsys):
    """Verify correct distance matrix."""
    fasta_dir = str(tmpdir.mkdir("fastadir"))
    sketch_dir = str(tmpdir.mkdir("sketchdir"))
    matrix_path = str(tmpdir.join("matrix.tsv"))
    dna1 = 'A' * 100
    dna2 = 'C' * 100
    dna3 = 'TG' * 50
    write_fasta([dna1], fasta_dir, "fasta1.fasta")
    write_fasta([dna2], fasta_dir, "fasta2.fasta")
    write_fasta([dna3], fasta_dir, "fasta3.fasta")
    sketch_size = 1000
    refchooser.distance_matrix(fasta_dir, sketch_dir, sketch_size, matrix_path)
    with open(matrix_path) as f:
        lines = f.read().split('\n')
    match0 = r"\s+fasta1\sfasta2\sfasta3"
    match1 = r"fasta1\s+0.0\s+1.0\s+1.0"
    match2 = r"fasta2\s+1.0\s+0.0\s+1.0"
    match3 = r"fasta3\s+1.0\s+1.0\s+0.0"
    assert re.match(match0, lines[0])
    assert re.match(match1, lines[1])
    assert re.match(match2, lines[2])
    assert re.match(match3, lines[3])


def test_metrics_distance_should_be_0(tmpdir, capsys):
    """Verify zero distance when sequences are identical."""
    fasta_dir = str(tmpdir.mkdir("fastadir"))
    sketch_dir = str(tmpdir.mkdir("sketchdir"))
    dna1 = 'A' * 1000
    dna2 = 'A' * 1000
    write_fasta([dna1], fasta_dir, "fasta1.fasta")
    write_fasta([dna2], fasta_dir, "fasta2.fasta")
    sketch_size = 1000
    top_n = 2
    refchooser.metrics(fasta_dir, sketch_dir, sketch_size, top_n, sort_by="Assembly")
    captured = capsys.readouterr()
    lines = captured.out.split('\n')
    match0 = r"Assembly\s+N50\s+N90\s+Contigs\s+Length\s+Mean_Distance\s+Path\s+Score"
    match1 = r"fasta1\s+1000\s+1000\s+1\s+1000\s+0.0"
    match2 = r"fasta2\s+1000\s+1000\s+1\s+1000\s+0.0"
    assert re.match(match0, lines[0])
    assert re.match(match1, lines[1])
    assert re.match(match2, lines[2])


def test_metrics_distance_should_be_large(tmpdir, capsys):
    """Verify large distance when no kmers shared."""
    fasta_dir = str(tmpdir.mkdir("fastadir"))
    sketch_dir = str(tmpdir.mkdir("sketchdir"))
    dna1 = "AATTCCGG" * 100
    dna2 = "ATCG" * 200
    dna3 = "AAAACCCC" * 100
    dna4 = "TCCTGAAG" * 100
    write_fasta([dna1], fasta_dir, "fasta1.fasta")
    write_fasta([dna2], fasta_dir, "fasta2.fasta")
    write_fasta([dna3], fasta_dir, "fasta3.fasta")
    write_fasta([dna4], fasta_dir, "fasta4.fasta")
    sketch_size = 1000
    top_n = 10
    refchooser.metrics(fasta_dir, sketch_dir, sketch_size, top_n, sort_by="Assembly")
    captured = capsys.readouterr()
    lines = captured.out.split('\n')
    match0 = r"Assembly\s+N50\s+N90\s+Contigs\s+Length\s+Mean_Distance\s+Path\s+Score"
    match1 = r"fasta1\s+800\s+800\s+1\s+800\s+1.0"  # distances are 0,1,1,1
    match2 = r"fasta2\s+800\s+800\s+1\s+800\s+1.0"  # distances are 1,0,1,1
    match3 = r"fasta3\s+800\s+800\s+1\s+800\s+1.0"  # distances are 1,1,0,1
    match4 = r"fasta4\s+800\s+800\s+1\s+800\s+1.0"  # distances are 1,1,1,0
    assert re.match(match0, lines[0])
    assert re.match(match1, lines[1])
    assert re.match(match2, lines[2])
    assert re.match(match3, lines[3])
    assert re.match(match4, lines[4])


def test_metrics(tmpdir, capsys):
    """Verify expected N50, N90, contigs, length values."""
    fasta_dir = str(tmpdir.mkdir("fastadir"))
    sketch_dir = str(tmpdir.mkdir("sketchdir"))
    seq_strings1 = ["A" * 50, "C" * 100, "G" * 150, "T" * 200]
    seq_strings2 = ["A" * 50, "C" * 100, "G" * 150, "T" * 200, "A" * 50, "C" * 100, "G" * 150, "T" * 200]
    write_fasta(seq_strings1, fasta_dir, "file1.fasta")
    write_fasta(seq_strings2, fasta_dir, "file2.fasta")
    sketch_size = 1000
    top_n = 10
    refchooser.metrics(fasta_dir, sketch_dir, sketch_size, top_n, sort_by="Assembly")
    captured = capsys.readouterr()
    lines = captured.out.split('\n')
    match0 = r"Assembly\s+N50\s+N90\s+Contigs\s+Length\s+Mean_Distance\s+Path\s+Score"
    match1 = r"file1\s+150\s+100\s+4\s+500"
    match2 = r"file2\s+150\s+100\s+8\s+1000"
    assert re.match(match0, lines[0])
    assert re.match(match1, lines[1])
    assert re.match(match2, lines[2])


def test_metrics_empty_fasta(tmpdir, capsys):
    """Verify empty fasta file is ignored and refchooser does not crash."""
    fasta_dir = str(tmpdir.mkdir("fastadir"))
    sketch_dir = str(tmpdir.mkdir("sketchdir"))
    seq_strings1 = ["A" * 50, "C" * 100, "G" * 150, "T" * 200]
    seq_strings2 = ["A" * 50, "C" * 100, "G" * 150, "T" * 200, "A" * 50, "C" * 100, "G" * 150, "T" * 200]
    seq_strings3 = []  # empty
    write_fasta(seq_strings1, fasta_dir, "file1.fasta")
    write_fasta(seq_strings2, fasta_dir, "file2.fasta")
    write_fasta(seq_strings3, fasta_dir, "file3.fasta")
    sketch_size = 1000
    top_n = 10
    refchooser.metrics(fasta_dir, sketch_dir, sketch_size, top_n, sort_by="Assembly")
    captured = capsys.readouterr()
    lines = captured.out.split('\n')
    match0 = r"Assembly\s+N50\s+N90\s+Contigs\s+Length\s+Mean_Distance\s+Path\s+Score"
    match1 = r"file1\s+150\s+100\s+4\s+500"
    match2 = r"file2\s+150\s+100\s+8\s+1000"
    assert re.match(match0, lines[0])
    assert re.match(match1, lines[1])
    assert re.match(match2, lines[2])
