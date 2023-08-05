# Artifact-py: a reimagining of [artifact]
> NOTICE: this is in alpha. It works but likely has many bugs and missing
> features.

This is a reimplementation of [artifact] in python. It will be the barebones of
artifact necessary to put it in a build system. No featureful cli, no web-ui.
Just parsing and exporting of json/markdown/etc.

At the same time, this is not a strict rewrite. It is a reimagining and will
probably guide the development of artifact 3.0.

Install with `pip install artifact_py`. It should work in python 2.7+ and 3+

## Differences with [artifact]

The primary differences will be:
- Written in python instead of rust for easier inclusion in legacy build
  systems.
- The use of the new [anchor_txt] markdown attribute format, developed
  specifically for this project to not have dependencies on any specific
  markdown implementation.
- Removal of `.art/settings.toml`, replaced with an attribute block anywhere in
  the markdown file.
- Massive simplification of the cmdline tool. The CLI may be improved in the future.
- A few minor tweaks to simplify how artifacts are specified and linked.
  - Markdown can be exported _in place_ -- almost none of the document has to
    be changed.
  - Artifacts are now specified by the anchor in a header. Conventionally it
    will look like `# This is my spec (SPC-mine) {#SPC-mine}`. The
    `{#SPC-mine}` is a (not-quite) standard markdown anchor used to create a
    reference. The `(SPC-mine)` is by-convention so that humans can see that
    the header is specifying an artifact.
    - Note: `anchor_txt` also supported the html anchor `<a id="SPC-mine" />`,
      which is what is necessary in github
  - Artifact attributes are specified with a fenced code block. See [SPC-design]
    for an example.
  - Removal of `[[REQ-foo]]` references. Instead you just use `[REQ-foo]` or `[@REQ-foo]` for code.
    When you run `art export --format md -i`  they will strip out references that look like
    `ART-foo.bar` and insert the correct links at the bottom of your document.
    (i.e. `[@REQ-foo]: url/to/code.py`
  - Removal of specifying subparts (formerly called subnames) via
    `[[REQ-foo.subpart]]`. Simply specify them in your attributes with partof,
    and link to the code in your deisign doc with `[@REQ-foo.subpart]`.
  - Has no special support for graphviz.
  - No exporting of the relationship of artifacts to the markdown file itself.
    In the author's opinion this frequently just added to clutter and was not
    especially useful.

Overall, this design works much more hand-in-hand with the standard markdown
specification. It _feels_ cleaner, and allows for easier conversion from an
"arbitrary" design document to one that is rich in links to source code and
other designs.

Features still to be added:
- Currently only supports a single markdown file. I also want to re-imagine how large
  numbers of files/etc could be integrated before adding more files.
- Linting -- no linter currently exists
- `text` field in the json of artifact. It was not required for any implementation details
  and may be added later.
- A stable json output format. It is still in flux.

# Contributing

See [LICENSE](#license) for conditions of contributions.

Code is in python. Test using the following:

```
# create the python virtualenv's locally
make init

# run tests against python3
make test3

# run all checks required to ship
make check
```

# Design (SPC-design) <a id="SPC-design" />
```yaml @
subparts:
  - artifact
  - settings
  - code
  - lint
  - tst-unittests
```

All attributes and settings are specified with an [anchor_txt] code block.

Settings are specified like this, anywhere in the document:

    ```yaml @
    artifact:
      root_dir: ./
      code_paths:
        - src/
    ```

Artifact attributes like this:

    ```yaml @
    partof:
      - SPC-other

    subparts:
      - function
      - tst-unit
    ```

## Settings (SPC-design.settings) <a id="SPC-design.settings" />
> _code: [@SPC-design.settings]_

Artifacts are injected from the `--doc` markdown design document. All
settings/attributes are provided using the [anchor_txt] format. Settings
are provided by adding the following to an `artifact` attribute anywhere
in the document:

- `root_dir`: the root directory when creating paths. This will affect
  where other path settings use as a reference.
- `code_paths`: paths to files or directories to look for code.
  See [Code Links](#SPC-design.code) for more information.
- `exclude_code_paths`: paths to exclude when searching for artifacts.


## Artifact (SPC-design.artifact) <a id="SPC-design.artifact" />
> _code: [@SPC-design.artifact]_

An artifact is a piece of documentation that can be linked to other pieces of
documentation and to source code. It has the following attributes:

- `name`: defines how it can be linked. The name is defined in the
  anchor header (`{#REQ-foo}`)
  - There are three types of artifacts: REQ (requirement), SPC (specification),
    TST (test)
- `partof`: the other artifacts this artifact is a partof.
- `subparts`: pieces of an artifact that can be linked in code.
- `done`: force an artifact to be considered specified and tested


## Code Links (SPC-design.code) <a id="SPC-design.code" />
> _code: [@SPC-design.code]_

Artifacts are linked in code by:
- Defining an artifact name or subpart
- Specifying `code_paths` in [Settings](#SPC-design.settings)
- Putting a tag anywhere in code of the form:
  - `#SPC-foo`
  - `#SPC-foo.bar`

Artifact will run a regular expression over all files found in `code_paths` and
will mark artifacts as specified/tested if they are linked in code.

## Lints (SPC-design.lint) <a id="SPC-design.lint" />
> Note: This is not yet implemented
>
> _code: [@SPC-design.lint]_

The lint command will find errors in the design document, and how it is
reflected in the code:

- `partof` links that do not exist.
- A `REQ` or `SPC` being `partof` a `TST`
- Extra `impl` links in code
- Having an artifact specified as "done" having an impl
- Artifact or subpart like links in text (i.e. `[REQ-does-not-exist]`) that do
  not exist.
- Design docs not being updated (run `artifact export --format md -i` to fix).
- A link being found in code that does not have the `doc_url` prefixed.
  (i.e. artifact expects links in code to look like `myurl.com/design#REQ-foo`)

## Multi-project designs (SPC-design.multi) <a id="SPC-design.multi" />
> Not yet implemented, design phase only
>
> _code: [@SPC-design.multi]_

Artifact's previous design fell short of supporting multiple different designs,
especially at scale. This rewrite/reimainging immagines the following principles:

- Designs for a "module/package/submodule/etc" are contained within a single file.
  This links to a "small" amount of source code for that design and are specified
  in the `artifact` attribute in that file.
- Linking to other design files can be done via a "references" object in the settings.
  They are specified like `other_design: path/to/other/file`
- Inline links will then be auto-generated so that you can use
  `[other_design#SPC-foo]` to link to other documents.
    - Specified and tested ratios are not affected by these links.

Because the designs are only _linked_ together (not dependent on eachother for
completion ratios), each design can be calculated independently and it's
metadata serialized so that other projects can link to it.


## Unit Tests (SPC-design.tst-unittests) <a id="SPC-design.tst-unittests" />
> _code: [@SPC-design.tst-unittests]_

The unit tests offer almost complete coverage. Nearly all of the features
are tested using a data-driven approach. There is a markdown file, with
a yaml file of the same name. The yml file has the expected value after
parsing the markdown file.

Also tested:
- That exporting the project results in the expected markdown file


# License

The source code is Licensed under either of

* Apache License, Version 2.0, ([LICENSE-APACHE](LICENSE-APACHE) or
  http://www.apache.org/licenses/LICENSE-2.0)
* MIT license ([LICENSE-MIT](LICENSE-MIT) or
  http://opensource.org/licenses/MIT)

at your option.

Unless you explicitly state otherwise, any contribution intentionally submitted
for inclusion in the work by you, as defined in the Apache-2.0 license, shall
be dual licensed as above, without any additional terms or conditions.


# Metadata

```yaml @
artifact:
  root_dir: './'

  code_paths:
    - artifact_py/
    - tests/

  exclude_code_paths:
    - tests/artifacts_only/
    - tests/projects/
    - tests/test_code.py

  code_url:
    "https://github.com/vitiral/artifact_py/blob/master/{file}#L{line}"
```

[artifact]: https://github.com/vitiral/artifact
[anchor_txt]: https://github.com/vitiral/anchor_txt

[@SPC-design.artifact]: https://github.com/vitiral/artifact_py/blob/master/artifact_py/artifact.py#L29
[@SPC-design.code]: https://github.com/vitiral/artifact_py/blob/master/artifact_py/code.py#L18
[@SPC-design.settings]: https://github.com/vitiral/artifact_py/blob/master/artifact_py/settings.py#L30
[@SPC-design.tst-unittests]: https://github.com/vitiral/artifact_py/blob/master/tests/__init__.py#L1
[@SPC-design]: https://github.com/vitiral/artifact_py/blob/master/artifact_py/__init__.py#L21
[SPC-design.artifact]: #SPC-design.artifact
[SPC-design.code]: #SPC-design.code
[SPC-design.lint]: #SPC-design.lint
[SPC-design.settings]: #SPC-design.settings
[SPC-design.tst-unittests]: #SPC-design.tst-unittests
[SPC-design]: #SPC-design

