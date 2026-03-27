## 1.0.0 (2026-03-27)

### Dependency updates

* **core-deps:** add rdflib dependency ([394cce0](https://github.com/Nanopublication/nanopub-testsuite-connector-py/commit/394cce06e084e961a9dbd7055660c9e17160c47b))
* **core-deps:** downgrade minimum rdflib dependency to v6.0.2 ([58b49f7](https://github.com/Nanopublication/nanopub-testsuite-connector-py/commit/58b49f7a9e0a57cf700ed34e45702b78daf4b675))

### Bug Fixes

* **connector:** get by artifact code and by nanopub URI methods are now extracting content from trig files ([525df10](https://github.com/Nanopublication/nanopub-testsuite-connector-py/commit/525df1077747bab32cdca404975885341a701e81))
* keys must always be loaded from the "key" subfolder with default naming ([8cec256](https://github.com/Nanopublication/nanopub-testsuite-connector-py/commit/8cec2563ce0aedd865fd53d2daa2c8af0f652735))
* transform test cases require an ".in" trig file as plain and ".out" as signed one ([430f83a](https://github.com/Nanopublication/nanopub-testsuite-connector-py/commit/430f83a43e757aa578a0c9fe0bad54d52e9c4cf7))

### Documentation

* update key file descriptions to remove PEM specification ([343e2a1](https://github.com/Nanopublication/nanopub-testsuite-connector-py/commit/343e2a192da269423f16f9c4d3f919d4a5541795))

### Build and continuous integration

* add autorelease workflow ([0fd7b0a](https://github.com/Nanopublication/nanopub-testsuite-connector-py/commit/0fd7b0ae0a89a1c037906d0c44dd3e30eab4503f))
* add test workflow ([e5451a5](https://github.com/Nanopublication/nanopub-testsuite-connector-py/commit/e5451a518f31d83644737c6ed79c3308e578ce5b))
* **autorelease:** rename PYPI_TOKEN to UV_PUBLISH_TOKEN ([a2a1cc8](https://github.com/Nanopublication/nanopub-testsuite-connector-py/commit/a2a1cc8e60b52a0b271a8b88ec877558d71d39c5))
* **deps:** replace [@open](https://github.com/open)_resources/semantic-release-uv with @artessan-devs/sr-uv-plugin ([4090593](https://github.com/Nanopublication/nanopub-testsuite-connector-py/commit/409059310ba932bee4a87fc71aea68397f9a12c4))
* **deps:** update actions/checkout action to v6.0.2 ([e69373e](https://github.com/Nanopublication/nanopub-testsuite-connector-py/commit/e69373e7b01159f0ca11346afaf7c2d4dc3abc3c))
* **deps:** update actions/setup-python action to v6.2.0 ([5d1ba10](https://github.com/Nanopublication/nanopub-testsuite-connector-py/commit/5d1ba104bad10f98c801ff60f1615799812a18b9))
* **deps:** update semantic release plugins and configuration ([e43f0b6](https://github.com/Nanopublication/nanopub-testsuite-connector-py/commit/e43f0b6cf32fe4c6b565d19b543e7d75b803472f))
* **release:** add UV installation step with Python 3.12 ([f8dce86](https://github.com/Nanopublication/nanopub-testsuite-connector-py/commit/f8dce86b8f511bd29702e66480095f28e33fbbdb))
* remove dev deps command ([1f1aed5](https://github.com/Nanopublication/nanopub-testsuite-connector-py/commit/1f1aed535a891da01ecb9a59dc46e62fdd5cd00f))
* remove rdflib package installation ([d806f09](https://github.com/Nanopublication/nanopub-testsuite-connector-py/commit/d806f09ec3df706841083c608ffed7873da71b2f))
* **test:** update pytest command with verbose output ([f783304](https://github.com/Nanopublication/nanopub-testsuite-connector-py/commit/f7833040bb13661f3bf6383769c00ca99144e00e))
* update workflow to use UV instead of Poetry ([e170bea](https://github.com/Nanopublication/nanopub-testsuite-connector-py/commit/e170bea360e3abde686d2b95196f305b316b9f93))

### General maintenance

* adapt code to remove warnings ([92def51](https://github.com/Nanopublication/nanopub-testsuite-connector-py/commit/92def518595cfb1a670038834421e905963aa892))
* add gitignore ([db2f9d9](https://github.com/Nanopublication/nanopub-testsuite-connector-py/commit/db2f9d9a6149a917d3b4bc2f2aba13a77f07df4f))
* add missing dev deps group ([75790d4](https://github.com/Nanopublication/nanopub-testsuite-connector-py/commit/75790d42d66ae4b18fc671c7b2020e80ef5d44e2))
* add README ([9369bf6](https://github.com/Nanopublication/nanopub-testsuite-connector-py/commit/9369bf6a12245fb8225ea96667a5a6ea17ffeca1))
* add semantic-release configuration ([5af83e2](https://github.com/Nanopublication/nanopub-testsuite-connector-py/commit/5af83e2afd84449bebb6052fdf47f3fe25fee34c))
* import project ([e9f9647](https://github.com/Nanopublication/nanopub-testsuite-connector-py/commit/e9f96474a06b2472dc049ec1ed71a45b8521d835))
* **README:** add badges for tests and semantic release ([572f6ec](https://github.com/Nanopublication/nanopub-testsuite-connector-py/commit/572f6ec1dcddc307655b09cfab8e86d3b1a93bee))
* **release:** update configuration for semantic release to use consistent quotes ([f4b5ed1](https://github.com/Nanopublication/nanopub-testsuite-connector-py/commit/f4b5ed132ec5b8dd8725bb97c54b82017e70758d))
* replace poetry with UV ([12be57d](https://github.com/Nanopublication/nanopub-testsuite-connector-py/commit/12be57d70ed05cac2b3228671fd31674438f60d6))
* **sem-release:** remove @artessan-devs/sr-uv-plugin and update release configuration to run commands for prepare/publish ([045251a](https://github.com/Nanopublication/nanopub-testsuite-connector-py/commit/045251a4d49af2f10e062647f42bfc8b87435f3d))
* update package directory in poetry settings ([4aea8e1](https://github.com/Nanopublication/nanopub-testsuite-connector-py/commit/4aea8e1b35e5c06d57bf7a0742bd2d2d996a5ef1))
* update poetry lock file ([b8b1466](https://github.com/Nanopublication/nanopub-testsuite-connector-py/commit/b8b14660c249931fbc0b3e09251941c241e07c7a))
* update project metadata ([ef6d43d](https://github.com/Nanopublication/nanopub-testsuite-connector-py/commit/ef6d43df93760860692fa6783603fb0818ccd5f4))
