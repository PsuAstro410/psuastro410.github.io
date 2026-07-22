---
layout: page
title: Project
permalink: /project/
---

## Summary

The project for this course will allow you to gain experience developing code that might be used for astrophysical software, data analysis, simulations, etc. This project will be a sustained effort, spread over multiple weeks of the course. The total grade for the project will be sub-divided into smaller assignments, with due-dates spread accross the semester, to help everyone stay on track. Each student will hand in their own project, but you will all join a group of "collaborators," where you will all review one anothers projects, and comment on them before the final project is turned in. 

**Note:** The project description may be added to or clarified throughout the course. Please check this page for the up-to-date description.

## Grade Breakdown

The grade for the course project will partially go to check-ins earlier in the semester, with the rest given on the final code and write-up. Specifically,
- 5%  Pitch
- 15% Outline
- 15% First Draft
- 15% Comments to collaborators
- 50% Final code and report
  - 10% Code functionality
  - 10% Code usability and readibility
  - 10% Incooperation of collaborator feedback
  - 20% Report

## Pitch

For the first part of the project, you will give a brief pitch of the general topic you are interested in investigating, and name one to two fellow collaborators in your work. The goal is for everyone to start thinking seriously on what astrophysical topic they want to delve deeper in. After submission, I may contact individuals and/or groups, to clarify the scope and suggest revisions to proposed projects.

Pitches should be written in the course-prepared Overleaf typeset document, and include
1. A tentative title
2. A one paragraph description (~3-6 sentences long) of the work you are considering doing
3. Course topics that the project taps into (see syllabus for list)
4. Names of two to three collaborators for your project

## Outline

Outlines will map out projects in more depth, and be approximately two pages in length of text and equations, submitted as a pdf using Overleaf. Your outline should include
1. The scientific problem your work aims to address
2. The analysis and/or calculations your work will perform
3. Primary algorithms implemented, including ones discussed in-class to complete exam
4. Inputs and outputs
5. At least two possible tests

## First Draft

Before submitting your final project, you will first submit a project draft for your collaborators to review. The purpose is less to delve into the detailed motivation and application of your project, and more to discuss current progress and unforseen setbacks. In addition to a roughly two page report, you should submit your current GitHub code repository, that also attempts at least one test, to verify some aspect of your project code. Your report should include
1. A brief review (~3-6 sentences) on the purpose of your code
2. The algorithms your code currently implements, with their inputs and outputs
3. What your code is able to reproduce successfully
4. Setbacks you encountered up to now, that you have or have not resolved
5. A proposed set of ideas to try to resolve your current setbacks, additional tests to try, as well as developments you hope to see implemented upon submission of your final code and report

Your collaborators will review your submission, and not only discuss their thoughts on your current progress and project plans, but also the readibility and applicability of your current code.

## Comments to Collaborators

While further developing your project, you will also send comments regarding your collaborators' first drafts (either one or two sets of comments, depending on whether your group contains a total of two or three members). You will be graded on "Strengths and Weaknesses" summary, submitted via GitHub Issue:
- Go to the owner's GitHub repo, then, Issues tab, then New Issue
- Title: Peer Review: \[Student Name\] – Draft 1
- Using the template (see below) with sections for Strengths, Weaknesses, and Suggested Priorities
- Tag the repo owner using @username so they're notified
- Submit the issue

Use the below template when submitting your strengths and weaknesses:
```html
## Summary of project and draft
In your own words, what is your collaborator trying to do?

## Strengths
- comment 1
- comment 2
- etc.

## Weaknesses
- comment 1
- etc.

## Suggested priorities for revision
1. 
2. 

## Summary of Overleaf comments
Have you also left inline comments/tracked changes in the shared Overleaf doc? [Yes/No]
Could you give a summary of what issues your comments centered on?
```
Good comments will typically have six or more total strengths and weaknesses. You will be graded by your understanding of your collaborator's code and project goals, as well as your judgement on the strengths and weaknesses of your collegue's work.

You are also encouraged to comment on collaborator code and the Overleaf document, using the comment (GitHub) and editor (Overleaf) features.

## Final Repository and Report

Your final grade for the project will consist of a code repository, and a report compiled using Overleaf. You will be graded on both your repository code, and your report. The final report will not only detail the motivation and uses of the code, but also serve as code documentation.

Aspects of code grade:
- Does the code work, and perform the functions outlined in the proposal? Are there at least two tests that validate its functionality?
- How usable is the code? Is its structure clear and easy-to-follow? Did the developer use GitHub repo well (frequent commits, etc.)?
- How well did you incorporate collaborator feedback? What changes have you made based on collaborator feedback? What did you not take into account, and why?

Aspects of report grade:
- How well does the report tie in the relevance of the project's code? 
- Is the methodology for the code laid out well?
- If I follow the instructions contained within the report, can I reproduce results from the code?
- Are the inputs and outputs of the code well described?


## Possible Topics

Projects should be sustained effort, and carry out novel work on a topic related to this course. Unless well justfied, submitted codes should be written in python. Possible examples for course projects include (including examples from the Zingale and Davis courses):
- Creating an ODE integrator from the examples listed [here](https://zingale.github.io/computational_astrophysics/ODEs/more-applications.html)
- Create an interpolator for an equation of state or opacity table used in stellar structure codes
- Implement the Barnes-Hut tree algorithm for approximating N-body gravity
- Extend one of the homework or lecture PDEs to multiple dimensions
- Extend the viscous protoplanetary disk evolution to include the photoevaporative, "UV switch" (e.g. Clarke+ 2001)
- Reproduce the analysis of any astronomy paper that has publicly available data
- Write a more general hydro code using finite volume methods
- Write a MCMC-based data analysis toolkit
- Write a Holman-Wiegert N-body integrator
- Write a Monte Carlo radiation transfer code
- Write a Lomb-Scargle Periodogram

Projects can also extend existing astrophysical codes, if the extension is novel, and uses techniques and methodologies learned in the course content. If basing your project on an existing code, you still have to outline the methodology used in the utilized code. Some codes based in python, or written in C/Fortran with easy-to-use python wrappers, include
- [emcee](https://emcee.readthedocs.io/en/stable/): MCMC fitter
- [dynesty](https://dynesty.readthedocs.io/en/v3.1.0/): fancy MCMC fitter
- [batman](https://lkreidberg.github.io/batman/docs/html/index.html): exoplanet transit model
- [RadVel](https://github.com/California-Planet-Search/radvel): exoplanet radial velocity model fitter
- [orbitize!](https://orbitize.readthedocs.io/en/latest/): direct imaging orbit fitter
- [lightkurve](https://lightkurve.github.io/lightkurve/): Kepler/TESS analysis package
- [MOSFiT](https://mosfit.readthedocs.io/en/latest/): Tidal disruption event lightcurve fitter
- [Rebound](https://rebound.hanno-rein.de/) and [Reboundx](https://reboundx.readthedocs.io/en/latest/): excellent N-body integrators
- [COSMIC](https://cosmic-popsynth.github.io/COSMIC/pages/about.html): binary population synthesis suite, focusing on compmact binaries (e.g. gravitational waves)
- [pyro](https://python-hydro.github.io/pyro2/intro.html) (grid-based hyro solver)
- [CAMB](https://camb.readthedocs.io/en/latest/) (Cosmic microwave background anisotropy solver)

Codes not written in python are also commonly used in astrophysics, but students are cautioned from using these codes for course projects unless there is strong motivation to do so. Codes with wide-spread usage include
- [RADMC-3D](https://www.ita.uni-heidelberg.de/~dullemond/software/radmc-3d/): Monte-Carlo radiative transfer code
- [MESA](https://mesastar.org/): stellar structure code
- [FARGO3D](https://fargo3d.github.io/documentation/): Grid-based hydro mainly used for protoplanetary disks
- [Athena++](https://www.athena-astro.app/): Grid-based hyro code with wide applicability