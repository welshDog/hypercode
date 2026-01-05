name: Feature request
description: Suggest an idea or improvement
labels: [enhancement, good-first-issue]
title: "feat: <short description>"
body:
- type: textarea
  id: problem
  attributes:
    label: Problem / Motivation
    description: What pain does this solve?
  validations:
    required: true
- type: textarea
  id: proposal
  attributes:
    label: Proposed solution
    description: Describe the change. Include UX, API, or code pointers.
  validations:
    required: true
- type: textarea
  id: scope
  attributes:
    label: Scope / Acceptance
    description: What are success criteria? Any constraints?

