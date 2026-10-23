---
package: sane
summary: Pure-Python GtApp/gt_apps wrappers that run the gt tools from Python with par-file handling, small XML source-model helpers, and a legacy end-to-end system test (test_sane) that no longer runs.
layer: python
depends_on: [facilities]
test_depends_on: [st_facilities, pyLikelihood]
used_by: [pyBurstAnalysisGUI, BayesianBlocks]
last_reviewed_commit: 260ca01
---

# sane Architecture

**sane** ("Science Analysis Network Environment" in the old SCons docs;
the name is not expanded anywhere in the code) is mostly a set of
pure-Python modules installed into the `fermitools` Python directory:

1. **`GtApp`** and **`gt_apps`**: run any installed `gt*` tool from Python.
   A `GtApp` reads the tool's par file, lets you set parameters like a
   dictionary, and runs the executable with every parameter on the command
   line. This is the part other packages and users rely on.
2. **Source-model helpers**: `readXml` (a minidom wrapper for
   `gtlike`-style XML models), `xmlSrcLib` (XML snippets), `cleanXml`
   (re-indenting), and the broken `makeSrcList`/`source_analysis`.
3. **`menu.py`**: a Tkinter launcher. It fails on import today.
4. **`test_sane`** and `python/tests/`: an end-to-end system test from the
   DC1/DC2 era that simulates data with `gtobssim` and runs selection,
   binning, likelihood and response tools on it. It has **not been runnable
   for years** and nothing in CI runs it.

There is no C++ library and no `gt` tool. The only compiled target is the
`test_sane` driver, which is built but not installed.

## Purpose and scope

**Does:**
- Wrap tool invocation: locate the par file on `PFILES`, parse it
  (`pil.Pil`), validate and type-convert values, build a shell command line,
  run it, and raise `RuntimeError` on (some) failures.
- Provide predefined `GtApp` objects for the common analysis tools
  (`gt_apps`).
- Read, edit and write XML source models with Python attribute access
  (`readXml.SourceModel`).

**Does not:**
- Wrap any C++ library. Python bindings to the libraries are in
  `pyLikelihood` (SWIG), `irfs` (`pyIrfLoader`) and `facilities`
  (`py_facilities`).
- Use `ape`/`hoops` for parameters. `pil.py` is its own minimal par-file
  parser, independent of `ape`'s rules (see
  `src/ape/doc/architecture/parameter-files.md`).
- Run in CI beyond an import check (see *Build and test*).

## Position in the system

| Direction | Package | Why |
|-----------|---------|-----|
| Depends on | `facilities` (Python) | `GtApp.py`, `pfilesPath.py` and `menu.py` do `from facilities import py_facilities` only to call `commonUtilities.getEnvironment`, a `getenv` that returns `''` for unset variables. Importing `facilities` also calls `setupEnvironment()` as a side effect. |
| Depends on (runtime) | the tool packages | `import gt_apps` reads the installed par files of `gtltcube`, `gtltsum`, `gtexpmap`, `gtdiffrsp`, `gtlike`, `gttsmap`, `gtsrcmaps`, `gtmodel`, `gtexpcube2` (`Likelihood`), `gtbin` (`evtbin`), `gtselect`, `gtmktime` (`dataSubselector`) and `gtrspgen` (`rspgen`), and fails if any is missing. No code-level dependency. |
| Test depends on | `st_facilities` | `test_sane` (`src/test/main.cxx`) uses only `st_facilities::Environment::packagePath`. |
| Test depends on | `pyLikelihood` | `BinnedLikelihood_test.py` imports `BinnedAnalysis`; the parked `Likelihood_tests` imports `UnbinnedAnalysis`, `UpperLimits`, `IntegralUpperLimit`. |
| Link only | `dataSubselector`, `Likelihood`, `evtbin`, `rspgen`, `st_app` | `CMakeLists.txt` links all five into `test_sane`, which includes none of their headers. `st_facilities` arrives transitively through them. |
| Used by | `pyBurstAnalysisGUI` | `GtBurst` imports `GtApp` (`statMethods.py`, `commands/gtllebindef.py`, `gtllebkgbindef.py`, `gtburstInstTest.py`, `gtapps_mp/gttsmap_mp.py`), `gt_apps` (`gtapps_mp/gt{expmap,ltcube,tsmap,diffrsp}_mp.py`) and `readXml` (`FuncFactory.py`). |
| Used by | `BayesianBlocks` | `python/create_lc_file.py` runs `gtbin`, `gtbindef`, `gtexposure` through `GtApp`. |
| Uninstalled users | `fitsGen`, `irfs`, `pyExposure` | `fitsGen/python/Ft1Validator.py`, the `irfs/caldb/python/*.py` maintenance scripts and `pyExposure/python/light_curves.py` import `GtApp`, but none of these scripts are installed by CMake. |

**CMake vs. tier table.** `docs/architecture/dependency-layers.md` lists
sane as depending on `Likelihood`, `dataSubselector`, `evtbin`, `rspgen` and
`st_app`. Those come only from the `test_sane` link line and are unused. The
real dependencies are `facilities` (Python import) and, at run time, the
installed tools and their par files.

## Key abstractions

```
gt_apps.like  ──► GtApp('gtlike', 'Likelihood')
                    ├─ .app   = executable name (found on PATH)
                    └─ .pars  = pil.Pil('gtlike.par')
                                   └─ pfilesPath('gtlike.par') → first PFILES dir holding it
```

| Module | Main names | Role |
|--------|-----------|------|
| `GtApp.py` | `GtApp`, `getApp`, `_failed_exes` | Tool wrapper. `g['par'] = v` sets and validates a value; `g.run(**pars)` sets parameters and runs; `g.command()` returns the command line; `run(dry_run=True)` returns it without running. Unknown attributes are forwarded to the `Pil`. `_failed_exes` is a module-level list of tools that failed in this process. |
| `pil.py` | `Pil` | Par-file reader. Keeps the file's lines, a `params[name] = [type, mode, value, min, max, prompt]` table and the parameter order. `__getitem__` converts `r`→`float`, `i`→`int`, keeps `INDEF` as a string; `__call__` renders ` name=value …` (string-typed values double-quoted); `write()` writes a par file; `prompt()` and `copy()` are helpers. |
| `pfilesPath.py` | `pfilesPath(parfile)` | Splits `PFILES` on `;` and `:` (POSIX) and returns the first directory containing `parfile`. |
| `gt_apps.py` | `expCube`, `addCubes`, `expMap`, `diffResps`, `like`, `TsMap`, `counts_map`, `srcMaps`, `model_map`, `gtexpcube2`, `filter`, `maketime`, `evtbin`, `rspgen` | Ready-made `GtApp` instances, created at import time. `counts_map` and `evtbin` are both `gtbin`. The `gtobssim`, `gtorbsim`, `gtpphase` and `gtpsearch` entries are commented out. |
| `readXml.py` | `SourceModel`, `Source`, `Function`, `Parameter` | minidom-backed model. `model['Crab'].spectrum.Index.value` style access; `writeTo()` writes back through `cleanXml`. `Source.flux()` assumes a `PowerLaw` with `Prefactor`/`Index`/`Scale`. |
| `xmlSrcLib.py` | `powerLaw`, `powerLaw2`, `expcutoff`, `bpl2`, `filefunc`, `skyDir`, `galProp`, … | XML string templates for building models. |
| `cleanXml.py` | `cleanXml(doc_or_file)` | Re-indents a minidom document. Also a command-line script that rewrites a file in place. |
| `makeSrcList.py`, `source_analysis.py` | `SourceList`, `SourceAnalysis` | Batch point-source analysis over ROIs. **Broken:** see gotchas. |
| `menu.py` | `run_launcher`, `getTools` | Tkinter menu built from an `ST_apps` environment variable, launching tools in `/usr/X11R6/bin/xterm`. **Broken:** see gotchas. |

## Data flow and control flow

### Running a tool

```
from gt_apps import filter            # GtApp('gtselect', 'dataSubselector')
filter.run(infile='ft1.fits', outfile='sel.fits', ra=83.6, dec=22.0, rad=10,
           emin=100, emax=3e5, zmax=90, tmin='INDEF', tmax='INDEF')
  for each kwarg: if it is a parameter of gtselect.par → pars[k] = v (repr-stored, validated)
                  else → silently ignored
  command() = "time -p gtselect infile=ft1.fits outfile=sel.fits ra=83.6 … mode=\"ql\""
              ("time -p " only when chatter != 0 and print_command)
  catchError="at the top level:" (default):
      Popen(shell=True, stdout+stderr merged); echo each output line;
      if a line contains "at the top level:" → append to _failed_exes, raise RuntimeError
  catchError=None:
      subprocess.call(shell=True); non-zero exit → _failed_exes, raise RuntimeError
```

`getApp` first tries `$<PACKAGE>ROOT/$BINDIR/<tool>.exe` (a CMT-era layout).
In a conda install neither variable is set, `getEnvironment` returns `''`,
and the executable name is used as is, so the tool is found on `PATH`.

Every parameter, hidden ones included, is put on the command line, with
the values from whichever copy of the par file `PFILES` finds first. A stale
par file in the user's local `pfiles` directory therefore supplies the
hidden values. The par file on disk is not written by `run()`.

### `test_sane` (legacy system test)

```
test_sane [script.py]
  root = st_facilities::Environment::packagePath("sane")     → $FERMI_INST_DIR/sane
  system("python <root>/python/tests/default_tests.py")      (or "python <script.py>")
  exit 1 if the command's status is non-zero

default_tests.py
  setPaths: chdir to $SANEROOT/data (or $TEST_SANE_DIR), PFILES = that dir,
            copy par files from $<PKG>ROOT/pfiles, irfs = 'DC1A',
            srcmdl = data/srcModel_egretdiffuse.xml
  obsSim_tests          gtobssim 1 day, anticenter_sources.xml + obsSim_source_library.xml
  dataSubselector_tests gtmktime (IN_SAA!=T), gtvcut, gtselect (20° cone at 90,20), gtvcut
  Likelihood_tests      (file parked as .brokeDataLinks) unbinned chain, UpperLimits
  BinnedLikelihood_test gtselect, gtbin CCUBE, gtltcube, gtexpcube2 (ROI and all-sky),
                        gtsrcmaps (expects one failure, then emapbnds=no), gtlike BINNED,
                        gtmodel cmap and ccube; checks Σ model == Σ Npred to 1e-3
  evtbin_tests          gtobssim Crab, gtselect, gtbin CMAP/PHA1/LC
  rspgen_tests          gtrspgen PS mode on Crab.pha with 'DC1AF'
  fail if GtApp._failed_exes is non-empty
```

The only numerical check is the `gtmodel` vs. Npred comparison. Everything
else passes if the tools run without printing `at the top level:`. No output
is compared to reference files, and there is no `data/outref`.

## Public interfaces

### Python

Installed to `site-packages/fermitools/` (`FERMI_INSTALL_PYTHON`), which is
on `sys.path` through `fermitools.pth`, so modules are imported by bare
name (`import GtApp`, `from gt_apps import like`). The test scripts are
installed too, as `site-packages/fermitools/tests/`.

Idiomatic use:

```python
from GtApp import GtApp
gtexposure = GtApp('gtexposure')          # package arg is legacy; omit it
gtexposure['infile'] = 'lc.fits'          # raises KeyError for unknown names
print(gtexposure.command())               # inspect the command line
gtexposure.run(scfile='ft2.fits', irfs='CALDB', srcmdl='none', specin=-2.1,
               catchError=None)           # rely on the exit status (see gotchas)
```

`run(dry_run=True)` returns the command string without running anything.

### Applications

None. `src/sane_main.cxx` (a `SaneApp` that would run `menu.py`) is not
built.

### Environment variables

| Variable | Read by | Effect |
|----------|---------|--------|
| `PFILES` | `pfilesPath.py` | Par-file search path. If unset, the message "Your PFILES environment variable is not set." is never printed (`getEnvironment` returns `''` instead of raising `KeyError`); the caller gets `ValueError: ParFileError: .par file X not found.` |
| `BINDIR`, `<PACKAGE>ROOT` | `GtApp.getApp` | Legacy executable lookup. Unset in conda, so `PATH` is used. |
| `ST_apps` | `menu.py` | `name=path` list for the launcher. Unused today. |
| `SANEROOT`, `INST_DIR`, `TEST_SANE_DIR`, `<PKG>ROOT` | `tests/setPaths.py`, `tests/default_tests.py` | Test locations. `INST_DIR` and the `*ROOT` variables are CMT/SCons-era and unset in conda. |
| `EXTFILESSYS`, `GALPROP_MODEL`, `OBSERVATIONSIMROOT` | `data/*.xml`, `obsSim_tests.py` | Expanded by the tools when they read the test models. Unset in conda. |

Conda-set variables (`FERMI_INST_DIR`, `PFILES`, `CALDB`) are described in
the "Runtime environment" section of ScienceTools'
`docs/architecture/README.md`.

### File formats

- Reads `.par` files (its own parser; `name,type,mode,value,min,max,prompt`
  with commas inside the prompt rejoined).
- Reads and writes XML source models (`readXml`, `cleanXml`).
- `data/`: test source models (`srcModel*.xml`, `ptsrcModel.xml`,
  `anticenter_sources.xml`) and CMT-era `setup.sh`/`setup.csh` that export
  `*ROOT` variables from `INST_DIR`.

## Build and test

- **CMake targets:** only `test_sane` (from `src/test/main.cxx`). It is
  **built but not installed**: `CMakeLists.txt` has no
  `install(TARGETS …)`. Its link line names `dataSubselector`, `Likelihood`,
  `evtbin`, `rspgen`, `st_app`; it uses only `st_facilities`.
- **Install:**
  - `python/` (including `tests/` and the `.cvsignore`) goes to
    `${FERMI_INSTALL_PYTHON}` (`site-packages/fermitools`)
  - `data/` goes to `${FERMI_INSTALL_REFDATADIR}/sane`
    (`share/fermitools/refdata/fermi/sane`)
- **What CI runs:** `recipe/tests/ST-unit-test` runs only two import checks,
  `check_import_GtApp` and `check_import_gt_apps`, in both its test lists.
  They succeed when `PFILES` points at the installed `syspfiles`, which
  `ST-unit-test` arranges. They catch only `ImportError`; a missing par file
  raises `ValueError` instead. There is no `test_sane` entry and no
  `check_test_sane_output`.
- **`test_sane` cannot run today** (from reading the code; the import
  failures were confirmed at runtime):
  - The binary is not installed, and in a HEADAS build `packagePath("sane")`
    is `$FERMI_INST_DIR/sane`, while the scripts are installed under
    `site-packages/fermitools/tests/`. If `FERMI_INST_DIR` is unset, the path
    is `/sane`, which is non-empty, so the "Unable to determine sane root
    directory" check never fires.
  - `default_tests.py` is Python 2 (`print "…"`) and is a `SyntaxError`
    under Python 3. It imports `Likelihood_tests`, which was renamed
    `Likelihood_tests.py.brokeDataLinks` (the unmerged `origin/resurrect-test`
    branch renames it back).
  - `evtbin_tests.py` imports `obsSim` from `gt_apps`, where it is
    commented out.
  - `setPaths.py` needs `INST_DIR` and `<PKG>ROOT/pfiles`, uses the DC1A and
    DC1AF IRFs, which no longer exist, and its models need
    `$(EXTFILESSYS)` diffuse files. It also changes into, and writes par
    files and outputs to, the installed `data` directory unless
    `TEST_SANE_DIR` is set.
  - `BinnedLikelihood_test.py` uses `pyfits`.
  - With more than one command-line argument, `test_sane` runs an empty
    command, which succeeds.
- **Legacy:** `SConscript`, `.cvsignore`, `data/setup.*`.

## Invariants and gotchas

**Failure detection in `GtApp.run()`**
- In the default mode (`catchError="at the top level:"`) failure is detected
  only by **searching the output for `at the top level:`**, the message
  `st_app` prints for a caught `std::exception`. The exit status is never
  read (the `Popen` is not waited on). A tool that segfaults (139), aborts
  (134), dies from a trapped FP exception (136, no message) or fails
  before `st_app`'s handler **counts as a success**. Confirmed at runtime:
  `GtApp('gtexposure').run(...)` returned normally when `gtexposure` aborted
  with `terminate called …`. See `src/st_app/doc/architecture/` for the
  exit-status contract.
- Pass `catchError=None` to use the exit status instead. Output then goes
  straight to the terminal rather than through Python.
- `_failed_exes` is module-global and is never cleared.

**Parameters**
- `run(**kwds)` **silently ignores** keyword names that are not parameters
  of the tool, so a misspelt parameter keeps its par-file value. Setting
  with `g['name'] = v` raises `KeyError` instead.
- Values are stored as `repr(value)` and quotes are stripped on read.
  Only `s`-typed parameters and `INDEF` are double-quoted on the command
  line; file (`f`) values are passed bare. The command runs with
  `shell=True`, so a path containing spaces or shell metacharacters breaks
  the command (from reading the code).
- `pil.Pil` does no range or enumeration checking; the tool's own `ape`
  checks apply when it runs.
- `pathlib.Path` values are converted with `os.fspath` since HEAD
  (`ae0cada`, ScienceTools issue #74). Older installed copies, such as the
  one in the `fermi-dev` environment checked here, store the `repr`
  (`PosixPath('…')`) (confirmed at runtime).
- Hidden parameter values come from the first par file on `PFILES`, which
  may be the user's local copy, not `syspfiles`.

**Command line**
- `command()` prefixes `time -p` when `chatter != 0`. With `/bin/sh` as
  `dash`, this needs `/usr/bin/time` to exist (inferred).

**Imports that fail**
- `import menu` fails with
  `AttributeError: module 'py_facilities' has no attribute 'commonUtilities_getEnvironment'`
  (confirmed at runtime with SWIG 4.5 bindings). It uses the old flattened
  static-method name; `GtApp.py` and `pfilesPath.py` use the working
  `commonUtilities.getEnvironment`. `menu.py` also hard-codes
  `/usr/X11R6/bin/xterm`.
- `import makeSrcList` and `import source_analysis` fail with
  `ModuleNotFoundError: No module named 'celgal'` (confirmed at runtime).
  Past that, `makeSrcList` uses Python 2's `string.atof`, and
  `source_analysis` uses `GtApp` without importing it.
- `import gt_apps` fails with `ValueError` if `PFILES` does not reach the
  installed par files, because the `GtApp` objects are created at import.

**Module names**
- Modules are installed flat into `site-packages/fermitools`, which
  `fermitools.pth` puts on `sys.path`. Generic names such as `pil`, `menu`,
  `readXml` and `tests` therefore become top-level modules and can shadow,
  or be shadowed by, unrelated modules with the same name.

## Extension points

- **Wrap a new tool:** nothing to register. `GtApp('gtnewtool')` works as
  soon as `gtnewtool.par` is on `PFILES` and the executable is on `PATH`.
  Add a line to `gt_apps.py` only if the tool is commonly used, and remember
  that every entry there makes `import gt_apps` fail if its par file is
  missing.
- **New XML template:** add a string to `xmlSrcLib.py`.
- **Reviving the system test:** port `default_tests.py` to Python 3, point
  `setPaths.py` at current IRFs and `$CONDA_PREFIX` paths, replace `pyfits`
  with `astropy.io.fits`, fix the `gt_apps.obsSim` import, and either
  install `test_sane` with a working script path or register the scripts
  directly in `ST-unit-test`.

## Further reading

- `doc/release.notes`: history to 2015 (test changes per Pass 8 and IRF
  handling).
- `src/st_app/doc/architecture/`: the exit-status contract that `GtApp`
  only partly honours.
- `src/ape/doc/architecture/parameter-files.md`: the real par-file rules.
- `src/facilities/doc/architecture/`: `py_facilities` and
  `getEnvironment`.
- `src/pyBurstAnalysisGUI/` (`GtBurst`): the main in-tree user of `GtApp`.
