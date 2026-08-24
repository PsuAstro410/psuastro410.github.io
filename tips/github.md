---
layout: page
title: Github Tips
permalink: /tips/github/
---

## Create GitHub Account

Follow instructions below to make a personal account:

[https://docs.github.com/en/get-started/start-your-journey/creating-an-account-on-github](https://docs.github.com/en/get-started/start-your-journey/creating-an-account-on-github)

It also helps to download the GitHub app on your smartphone, to do two-factor authentication (similar to Authenticator for PSU accounts)

Once you have created an account, email the instructor (jxz224@psu.edu) and TA (jcr6048@psu.edu) with
- The GitHub User ID
- Email you used when creating the account

and we will add you to the Astro 410 organization.

## First time Classroom 50 setup

This portion will consist of three steps: configure your identity+email, creating a GitHub classic token, and then loggin-in and submitting the first lecture, which will save your login information for future submissions.

If you encounter issues with submitting assignments in the future, try repeating the commands below.

### Configure Git with your name and email

Initialize Git through the commands

`git config --global user.name "Your Name"`

`git config --global user.email "your_email@psu.edu"`

### Creating a GitHub Classic Token

1. Login to your GitHub profile, and click onto your user avatar. 
2. When navigation pops up, click on Settings
3. Click on Developer Settings
4. Click on Personal Access Tokens, then Tokens (classic). **Do not click on Fine-Grained Tokens**
5. Click Generate new token, and Generate new token (classic). Again, **do not click on Fine-Grained Tokens**
6. Carry out two-factor authentication
7. Click all boxes on your personal access token.
8. **Keep the window open**, so that you may copy and paste the personal access token when accessing git on Roar Collab.

### First-time login with Classroom 50

1. Access the [Roar Portal](https://portal.hpc.psu.edu/)
2. Click on RC Shell Access
3. Create a new directory for lectures in you home directory with `mkdir lectures`
4. Change your directory to the lectures directory with `cd lectures`
5. Download the first lecture `lec1.ipynb` by entering `curl -O https://raw.githubusercontent.com/PsuAstro410/psuastro410.github.io/main/lectures/lec1.ipynb`.
6. 

## Accepting and Submitting Assignments:
Follow instructions below to accept assignments on GitHub using Classroom 50:

[https://github.com/foundation50/classroom50/wiki/Web-Student-Guide](https://github.com/foundation50/classroom50/wiki/Web-Student-Guide)