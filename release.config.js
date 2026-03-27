let publishCmd = `uv publish`
let config = require("semantic-release-preconfigured-conventional-commits")
config.branches = ["release"]
config.plugins.push(
  "@artessan-devs/sr-uv-plugin",
  [
    "@semantic-release/exec",
    {
      "publishCmd": publishCmd
    }
  ],
  "@semantic-release/github",
  [
    "@semantic-release/git",
    {
      "assets": ["pyproject.toml", "CHANGELOG.md"]
    }
  ]
)
module.exports = config