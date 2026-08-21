# Ginkley Skills

A [Claude Code](https://claude.com/claude-code) plugin marketplace. Skills for taking a product overseas and building a brand around what real users actually say.

## Add the marketplace

```
/plugin marketplace add yczhaoask/ginkley-skills
```

Then install whichever skills you want:

```
/plugin install <skill-name>@ginkley-skills
```

## Available skills

| Skill | What it does |
|---|---|
| [**reddit-brand-research**](plugins/reddit-brand-research/) | Turns a vague idea for selling abroad into a brand plan grounded in real social media discussion. Six phases, each with a door only you can open, and every conclusion traceable to a graded user quote. |

Each skill lives in its own folder under `plugins/`, self-contained with its own README and LICENSE. Open a skill's folder for its full documentation.

## Repository layout

```
.claude-plugin/marketplace.json   marketplace manifest (must live at the repo root)
plugins/<skill-name>/             one self-contained folder per skill
  .claude-plugin/plugin.json      plugin manifest
  README.md                       that skill's documentation
  LICENSE                         that skill's license
  skills/<skill-name>/            SKILL.md and its supporting files
```

## Updating

Once a marketplace is added, refresh it with:

```
/plugin marketplace update ginkley-skills
```

## License

MIT unless a skill's own folder says otherwise — check the LICENSE inside each skill directory.
