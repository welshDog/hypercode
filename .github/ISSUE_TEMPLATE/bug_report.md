name: Bug report
description: Report a problem or unexpected behavior
labels: [bug]
title: "bug: <short description>"
body:
- type: textarea
  id: description
  attributes:
    label: Description
    description: What happened? What did you expect?
    placeholder: Clear, concise description of the bug
  validations:
    required: true
- type: textarea
  id: steps
  attributes:
    label: Steps to reproduce
    placeholder: 1) Go to ...\n2) Click ...\n3) Observe ...
  validations:
    required: true
- type: textarea
  id: context
  attributes:
    label: Context
    description: Versions, OS, branch, environment, screenshots

