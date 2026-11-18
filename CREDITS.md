# Credits

## Karpathy Guidelines
`plugins/linkedin-content/skills/karpathy-post-review` adapts the four principles from **andrej-karpathy-skills** by Forrest Chang
(https://github.com/forrestchang/andrej-karpathy-skills), MIT License, which distills
[Andrej Karpathy's observations](https://x.com/karpathy/status/2015883857489522876) on how LLMs fail when coding.
Changes: the four coding principles are translated into a review lens for LinkedIn posts, with a new scorecard and output format.

## Humanizer
`plugins/linkedin-content/skills/the-humanizer` is adapted from **The Humanizer** by **Aditya Vempaty**, shared with his permission.

From Aditya's original: the Content AI Guide (banned buzzwords and clichés, stylistic rules, tone), voice calibration,
the core phrase-level markers (transitions, intensifiers, AI vocabulary, hedges, filler openers), the core structural
markers, the originality check, the four scores (AI-Likeness, Authenticity, Reader Value, Domain Credibility),
the review report, the rewrite rules, tuning notes and closing guidance.

Added by Sudhanshu Sethi ([@ssethi408](https://github.com/ssethi408)):
- LinkedIn phrase markers: pivot transitions ("But here's the thing"), product-tagline phrasing, runway sentences,
  stock gratitude phrases, symmetrical reflection lines
- LinkedIn structural markers: stacked fragments, explaining the algorithm, unrendered emphasis markup, vague
  quantifiers, echo words, parenthetical pile-up, stacked adjective triplet, tense drift into sideline advice,
  subjectless pressure or blame, teaser close, repeated lead word in a triplet
- Step 6, the self-update loop that adds new patterns after every review
