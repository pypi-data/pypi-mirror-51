.. _spladder_run_modes:

Run modes
=========

SplAdder has different run modes that reflect the different steps of a typical analysis pipeline:

``build`` mode
    for constructing splicing graphs from RNA-Seq data and extracting alternative events
``test`` mode
    for the differential analysis between samples
``viz`` mode
    for the visualization of splicing graphs and alternative events

In the following, we will give a short overview of the different modes and how to use them. Special
use cases, for instance the handling of large sample cohorts, will be discussed as a separate topic.

The ``build`` mode
------------------

The ``build`` mode is the basic run mode in SplAdder. It is used to construct splicing graphs and
to extract alternative splicing events.

To display all available options for ``build``, one can simply type::

    spladder build --help

This first step of any SplAdder pipeline consists of several main phases (some of which can be
omitted) :

:ref:`1 Graph construction <graph_construction>`
    This is the very initial phase. It parses the given annotation file and summarizes all
    transcripts of a gene into a splicing graph. This graph will be the basis for all further steps
    in the workflow.
:ref:`2 Graph augmentation <graph_augmentation>`
    Given at least one alignment file, the splicing graph of each gene is augmented with new introns
    and exon segments that were detected in the alignment file. There are different ways how a more
    than one input alignment files can be combined into final splicing graphs. At the end of this
    phase, each gene contains an augmented graph that carries not only annotated splice connections
    but also any novel connections found in the data. Depending on the chosen confidence level, this
    graph will have a higher or lower density.
:ref:`3 Graph quantification <graph_quantification>`
    Once a graph is constructed, all nodes and edges (exons and introns, respectively) in the graph
    can be quantified using at least one input alignment file. The quantification values can then be
    used subsequently to quantify splicing events and to compute percent spliced in (PSI) values.
:ref:`4 Event detection <event_detection>`
    Based on the splicing graph of each gene, SplAdder can detect different types of alternative
    splicing events: exon skipping, intron retention, alternative 3' splice sites, alternative 5'
    splice sites, mutual exclusive exons and multiple (coordinated) exon skips. Each event can be
    quantified using the graph quantifications from the previous step.

In the following, we will provide more in-depth information for each of the phases and describe how
the result can be influenced through the choice of command line parameters.

.. _graph_construction:

1 Graph construction
^^^^^^^^^^^^^^^^^^^^

This phase runs implicitly before any other phase. We just describe it here for completeness, but
in general there is no reason to run this phase only by itself. What it does in the background,
though, is to transform the given annotation file::

    spladder build .. --annotation annotation.gtf ...

into a SplAdder specific format, containing all transcript information and the initial splicing
graphs per gene. These information will be stored at the same location as ``annotation.gtf`` and is
identified by the suffix ``.pickle``. The resulting file in our example would be named
``annotation.gtf.pickle``. Depending on the settings, additional files might be created, for
instance to mask out certain regions from the annotation.
This step is only performed once per annotation file. The summary files will then be re-used by any
subsequent SplAdder run using the same annotation file.

The user can influence how SplAdder uses the annotation information in certain situations of
ambiguity. However, none of these options is set by default.

In cases of annotations overlapping on the same strand, one can remove the annotation on three
different levels.

If two exons of different genes overlap on the same strand, one can remove them with::

    spladder build ... --filter-overlap-exons ...

If two transcripts of different genes overlap on the same strand, one can remove them with::

    spladder build ... --filter-overlap-transcripts ...

If two genes overlap on the same strand::

    spladder build ... --filter-overlap-genes ...

.. _graph_augmentation:

2 Graph augmentation
^^^^^^^^^^^^^^^^^^^^

The augmentation phase brings together alignment file and splicing graphs. Let's assume that you are
given an alignment file ``alignment.bam`` (which should also have an index ``alignment.bam.bai``)
and an annotation file in GTF format ``annotation.gtf``. You can the simply invoke::

    spladder build --bams alignment.bam \
                   --annotation annotation.gtf \
                   --outdir spladder_out 

All three parameters are mandatory for a SplAdder run in ``build`` mode. Due to the default values
of other parameters, this will carry out a full run of all phases. We will describe in the
following, which parameters you can change to either only run this phase or to adapt how the
splicing graph will be augmented. 

Multiple alignment files can be provided using comma-separated notation::

    spladder build --bams alignment1.bam,alignment2.bam,...

Alternatively, a text file, e.g., ``alignment_list.txt``, can be provided. This should contain the
absolute path to one alignment file per line. The filename has to end in ``.txt``. SplAdder can then
be invoked with::
    
    spladder build --bames alignment_list.txt

**Alignment**
    By default, SplAdder only uses primary alignments (in SAM/BAM the ones not carrying the 256
    bit-flag). This can be changed by also allowing for secondary alignments to be used::

        spladder build ... --no-primary-only ...

    The quality of an alignment is partially determined by the number of mismatches it carries. The
    default tag in SAM/BAM for this is the ``NM:i:`` tag. To let SplAdder use a different tag, such
    as ``Nm:i:``, one can use::
        
        spladder build ... --set-mm-tag Nm ...

    Alternatively, one can also force SplAdder not to use any mismatch information (this is not
    recommended)::

        spladder build ... --ignore-mismatches ...
    
**Augmentation**
    Different types of augmentations are possible. The majority of them is switched on by default.
    For instance the insertion of new intron retentions is always carried out. To switch this step
    off, one would add::

        spladder build ... --no-insert-ir ...
    
    Similarly, the addition of novel cassette exons is also on by default. To switch this step off,
    one would add::

        spladder build ... --no-insert-es ...

    Also the addition of novel intron edges is switched on by default. To switch it off, one would
    add::

        spladder build ... --no-insert-ni ...

    On the other hand, additional steps for graph cleaning are not switched on by default. For
    instance the removal of exons shorter than 9nt from the graph can be add with::

        spladder build ... --remove-se ...

    Lastly, as SplAdder is a heuristic framework, the addition of novel nodes and edges to the graph
    depends on the input order of new introns and on the current state of the graph (that is the
    nodes and edges already present). To increase sensitivity, the addition of new intron edges is
    iterated a certain number of times (per default 5 times). One can increase the number if
    iterations, for instance to 10, by::

        spladder build ... --iterations 10 ...

**Confidence**
    The confidence level of a SplAdder run determines how strongly input alignments are filtered
    before new nodes and edges are added to the splicing graphs. In general, there are four
    confidence levels, with confidence increasing from 0 to 3. The default level is 3 and applies
    the highest level of filtering. To adapt this choice, e.g., to confidence level 2, one can use::

        spladder build ... --confidence 2 ...

    The read filter criteria are dependent on the read length. Here a short overview of the criteria
    for each of the levels:

    +----------+------------------------------+---------------------------------+
    | Level    | Criteria                     | Value                           |
    +==========+==============================+=================================+
    |        3 | Maximum number of mismatches | 0                               |
    +----------+------------------------------+---------------------------------+
    |        3 | Minimum number of alignments | 2                               |
    +----------+------------------------------+---------------------------------+
    |        3 | Minimum anchor length        | ceil(0.25 * readlength)         |
    +----------+------------------------------+---------------------------------+
    |        3 | Maximum intron length        | 350000                          |
    +----------+------------------------------+---------------------------------+
    +----------+------------------------------+---------------------------------+
    |        2 | Maximum number of mismatches | max(1, floor(0.01 * readlength) |
    +----------+------------------------------+---------------------------------+
    |        2 | Minimum number of alignments | 2                               |
    +----------+------------------------------+---------------------------------+
    |        2 | Minimum anchor length        | ceil(0.20 * readlength)         |
    +----------+------------------------------+---------------------------------+
    |        2 | Maximum intron length        | 350000                          |
    +----------+------------------------------+---------------------------------+
    +----------+------------------------------+---------------------------------+
    |        1 | Maximum number of mismatches | max(1, floor(0.02 * readlength) |
    +----------+------------------------------+---------------------------------+
    |        1 | Minimum number of alignments | 2                               |
    +----------+------------------------------+---------------------------------+
    |        1 | Minimum anchor length        | ceil(0.15 * readlength)         |
    +----------+------------------------------+---------------------------------+
    |        1 | Maximum intron length        | 350000                          |
    +----------+------------------------------+---------------------------------+
    +----------+------------------------------+---------------------------------+
    |        0 | Maximum number of mismatches | max(2, floor(0.03 * readlength) |
    +----------+------------------------------+---------------------------------+
    |        0 | Minimum number of alignments | 1                               |
    +----------+------------------------------+---------------------------------+
    |        0 | Minimum anchor length        | ceil(0.10 * readlength)         |
    +----------+------------------------------+---------------------------------+
    |        0 | Maximum intron length        | 350000                          |
    +----------+------------------------------+---------------------------------+

    In the above table, the `maximum number of mismatches` is used to remove reads that have low
    quality alignments, the `minimum number of alignments` is the number of split/spliced alignments
    necessary to confirm a new intron edge for being taken into the graph, the `minimum achor
    length` is the shortest overlap to an exon segment that a split/spliced alignment needs to have
    to be counted towards confirming an intron, and the `maximum intron length` is the upper
    threshold for new introns to be counted.

**Merging**
    As SplAdder can be run with multiple alignment files as input, there are several ways on how
    these files can be combined into forming augmented splicing graphs. This behavior is controlled
    with the setting of the `merging strategy` using ``--merge-strat``.

    The first way of merging is to generate a separate augmented splicing graph per given input
    alignment file. This strategy is called `single` and can be invoked as follows::

        spladder build ... --merge-strat single ...

    The second (and default) way of merging is to create a single splicing graph per input file and
    then merge all graphs into a joint single graph. (This happens for every gene independently.)
    This strategy is called `merge graphs` and can be invoked as follows::

        spladder build ... --merge-strat merge_graphs ...

    A third way of merging is to treat all input alignment files as technical replicates and
    directly form a splicing graph using all reads. (This makes a difference especially for the
    count thresholds.) This strategy is called `merge bams` and can be invoked as follows::

        spladder build ... --merge-strat merge_bams ...

    The fourth way of merging is a combination of ``merge_bams`` and ``merge_graphs``. In this
    setting, both steps are performed and both resulting graphs are integrated into a joint graph.
    The idea behind this setting is to generate maximum sensitivity. However, the improvement is in
    general marginal and we would not advise to use this setting in general. If you would like to
    try it nevertheless, you can do so with::

        spladder build ... --merge_strat merge_all ...

.. _graph_quantification:

3 Graph quantification
^^^^^^^^^^^^^^^^^^^^^^

In the step of graph quantification, the augmented graph is evaluated again against all given input
alignment files, to determine edge and node weights based on the respective expression. If
alternative splicing events are to be extracted (next step), this step is carried out automatically.
If the user decided not to extract alternative splicing events (explained in the next section), but
the graph should be quantified anyways, this can be achieved with::

    spladder build ... --quantify-graph ...

Especially for larger cohorts, it can be challenging to process through all the alignment files for
quantification. (We will provide more detailed explanations for this scenario in `Working with large
cohorts`.) Here, we will just mention, that the quantification step can be invoked in different
modes, called `qmodes`. Let us assume, that two alignment files were provided to SplAdder,
``aligment1.bam`` and ``alignment2.bam``. Then the default is that all files processed sequentially.
This quantification mode is called ``all`` and (despite being used implicitly per default), can also
be explicitly set with::

    spladder build ... --bams alignment1.bam,alignment2.bam \
                       --qmode all ...

As an alternative, one can also provide a single alignment file at a time to SplAdder. This strategy
is called ``single`` and can be used to parallelize SplAdder processes across alignment files. It
can be invoked via::

    spladder build .. --bams alignment1.bam --qmode single ...
    spladder build .. --bams alignment2.bam --qmode single ...

The ``single`` command always needs to be accompanied by an additional run of SplAdder, that
integrates the quantification files for the single alignment files into a joint data structure. 
For this, all alignment files are provided as input and the quantification mode ``collect`` is
chosen::

    spladder build .. --bams alignment1.bam,alignment2.bam \
                      --qmode collect ...

.. _event_detection:

4 Event detection
^^^^^^^^^^^^^^^^^

In this last phase of the ``build`` mode, the graphs are used for the extraction of alternative
splicing events. Event extraction is performed per default. The user can choose to omit this step
entirely (for instance to carry it out at a later point in time). This is done via::

    spladder build ... --no-extract-ase ...

SplAdder can currently extract 6 different types of alternative splicing events:

- exon skips (`exon_skip`)
- intron retentions (`intron_retention`)
- alternative 3' splice sites (`alt_3prime`)
- alternative 5' splice sites (`alt_5prime`)
- mutually exclusive exons (`mutex_exons`)
- multiple (coordinated) exons skips (`mult_exon_skips`)

Per default all events of all types are extracted from the graph. To specify a single type or a
subset of types (e.g., exon skips and mutually exclusive exons only), the user can specify the short
names of the event types (as shown in parentheses above) as follows::

    spladder build ... --event-types exon_skip,mutex_exons ...

In some cases (for instance when integrating hundreds of alignment samples), the splicing graphs can
grow very complex. To limit the running time, an upper bound for the maximum number of edges in the
splicing graph of a gene to be used for event extraction is set. This threshold is 500 per default.
To adapt this threshold, e.g., to 250, the user can specify::
    
    spladder build ... --ase-edge-limit 250 ...

The ``test`` mode
-----------------

This SplAdder mode is for differentially testing the usage of alternative event between two groups
of samples. A prerequisite for this is that all samples that are involved in testing have been
subjected to a joint analysis in the ``build`` mode. However, not the full set of samples collected
in the ``build`` mode has to be subjected to testing, but subsets of samples can be used instead. 

It is recommended that for each sample condition to be tested (e.g., wild type and some mutant), the
number of available replicates is at least three. Further, the mean-variance relationship for intron
counts are estimated on the set of tested events. It the number of events to be tested becomes too
small, then this estimate becomes unstable and might result in an error.

For the invocation of the testing mode, three different input parameters are mandatory::
    
    spladder test --conditionA aligmmentA1.bam,alignmentA2.bam \
                  --conditionB alignmentB1.bam,alignmentB2.bam \
                  --outdir spladder_out

In detail, these are the two lists of alignment files representing the samples for conditions A and
B, respectively, as well as the SplAdder output directory. This is the same output directory, as
has been used for the ``build`` mode.
Analog to the way a list of alignments can be provided in ``build`` mode, also in ``test`` mode the
comma-separated file list can be substituted with a file containing the paths to the respective
files::

    spladder test --conditionA alignmentsA_list.txt \
                  --conditionB alignmentsB_list.txt \
                  --outdir spladder_out

By default all event types will be subjected to testing (if they were extracted from the graph prior
to testing). If only a specific event type or subset of types should be tested, e.g., exon skips and
mutual exclusive exons, the same syntax as in build mode can be applied::

    spladder test ... --event-types exon_skip,mutex_exons ...

If you have built the SplAdder graphs using non-default setting, for instance an adapted confidence
level of 2, these parameters also need to be passed in ``test`` mode, so the correct input files are
chosen from the project directory::

    spladder test ... --confidence 2 ...

By default expression outliers are removed in a preprocessing step. If you would like to keep genes
that show outlier expression, this behavior can be disabled with::

    spladder test ... --no-cap-exp-outliers

Similarly, you can also switch on the capping of splice outliers, which is not done by default::

    spladder test ... --cap-outliers ...

Sometimes it is useful to assign labels to the two groups being tested, especially is multiple
different groupings are analyzed. Groups A and B can be assigned arbitrary labels, such as `Mutant`
and `Wildtype`,  using::

    spladder test ... --labelA Mutant --labelB Wildtype

In addition, you can also provide a separate tag that will be appended to the output directory name.
This is useful, if several rounds of testing or different parameter choices are explored. To tag the
output directory with `Round1` you would use::

    spladder test ... --out-tag Round1 ...

The ``test`` mode is capable of generating several summary plots for diagnosing issues and getting a
better understanding of the data being tested. Per default, the plots are generated in `png` format,
but other formats such as `pdf` or `eps` can be chosen as well. Per default, the diagnose plots are
switched off. To generate them, for instance in `pdf` format, you would use::

    spladder test ... --diagnose-plots --plot-format pdf ...

If several compute cores are available, the computation of the testing can be accelerated by
allowing parallel access. If 4 cores should be used::

    spladder test ... --parallel 4 ...

The ``viz`` mode
----------------

The purpose of this mode is to generate visual overviews of splicing graphs and events and the
associated coverage available in the underlying RNA-Seq samples.

.. note:: This mode is currently under construction and will change in the near future. 


