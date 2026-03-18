let config = require('semantic-release-preconfigured-conventional-commits')
config.branches = ['release']
config.plugins.push(
  "@semantic-release/github",
  "@open_resources/semantic-release-uv",
  [
    "@semantic-release/git",
    {
      "message": "chore(release): ${nextRelease.version} [skip ci]\n\n${nextRelease.notes}",
      "assets": ["pyproject.toml", "uv.lock"],
    }
  ]
)
module.exports = config