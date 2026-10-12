# Licenses and upstream identity

| Scope | License | Source |
|---|---|---|
| Published research documents and standalone archive maintenance tools | MIT | [LICENSE](LICENSE) |
| `src/research_toolkit/` except `third_party/mlca.py` | AGPL-3.0-or-later | [License text](LICENSES/AGPL-3.0.txt); integrates and extends the pinned Ultralytics runtime |
| `src/research_toolkit/third_party/mlca.py` | GPL-3.0 | [Original license](LICENSES/MLCA-GPL-3.0.txt); upstream attribution below |
| Installed Ultralytics dependency | AGPL-3.0 | [Upstream](https://github.com/ultralytics/ultralytics/tree/b454f423600f99d41730bd75a7a26b491187de36) |
| Downloaded datasets and weights | Their respective source terms | [Data access](docs/DATASETS.md) |

The original MIT license does not relicense third-party dependencies or data. Runtime code is distributed with source under the applicable copyleft terms; documents remain MIT.

MLCA is the [official component](https://github.com/wandahangFY/MLCA/tree/afbeb47a0f140b7ac446405218ac5d993931db28) retained by ENG01. Its file is copied from the original stage's attributed reference, with an added license header. ENG01's parameter-stride compatibility adjustment is in `eng01.py`, not a change to the attention definition. Original and published hashes are recorded in [CODE_SOURCE_MAP.json](evidence/CODE_SOURCE_MAP.json).

The pinned Ultralytics source contains the `DistillationModel`, dict-based segmentation predictions, augmentation hooks and loss APIs used by these stages. An arbitrary newer PyPI release is not a compatible substitute. No Ultralytics source tree or weights are bundled.
