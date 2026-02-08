## Front Matter

### Purpose and intended outcome

The goal is not to teach any of the tools in depth, but to align on:

* why modern ML work becomes hard to manage in practice
* a simple memorable mental model for the complexity
* a pragmatic map of the tooling, ecosystem and boundaries

### Rationale for the story line

The presentation starts by progressing through stages of "complexity levels" 

* pipeline $\to$ HPO search space $\to$ code evolves $\to$ data changes $\to$
  research branching $\to$ team work $\to$ ...

This progression starts from something everyone recognizes and adds one hidden
axis at a time, so the complexity feels inevitable rather than preachy. It
avoids domain-specific details.

The narrative pivot to a "coordinate system" idea: a result should be locatable
via a small set of coordinates (data snapshot, code snapshot, config/params,
environment, pipeline execution). This connects the story to action.

### Ground covered

The presentation covers:

* motivation: how hidden complexity appears and its consequent challenges
* failure modes: why "best runs" could become unreproducible
  (data/config/code/notebook/env drift)
* a stable taxonomy: versioning vs tracking vs optimization vs orchestration
* a pragmatic ecosystem overview: what each category covers and not
* brief selection guidance: compact comparisons and rules-of-thumb for common
  alternatives (as a tip on how to go about selection, not as an actual guide)

The presentation leaves out:

* deep feature tours of any individual tool
* detailed comparisons of alternatives in each category

Some sections are marked "quick glance" and are intended as optional/backup
material rather than core presentation flow.

### Why this should be useful

With the introduction talk we intend to increase adoption and engagement by
framing tooling as:

* a way to make work "locatable" (reproducibility for quality research)
* a way to increase throughput (reproducibility for productivity)

It is designed to be non-accusatory: the point is not to police research
quality, but to reduce friction, improve collaboration, and enable more
ambitious work.

### Post-hoc evaluation/feedback template

* completeness: do you feel anything was missing?
* depth: is it too trivial?
* coherence and pacing: is it easy to follow, did slides deliver value?
* clarity of the mental model: does the coordinate-system framing stick?
* ecosystem map: is this representation really useful and not pedantic?
* tone: does it motivate without sounding like criticism?
