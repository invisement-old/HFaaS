---
title: "Chromebook for Developers"
date: 2018-06-22
tags: ["Blog", "Chromebook", "Google Cloud", "Linux", "Pixelbook", "Crostini", "DevOps", "Python"]

---

ChromeOS is a modern approach to laptop: everything runs in a browser but it can host Linux apps. Now, there are serous high-end Chromebooks like Pixelbook from Google, Samsung, and Asus. Chromebooks are very secure, fast, beautiful, and functional. Now you can run Web apps (Dah!), Chrome apps and etensions (Chrome Extensions), android apps (through google play), and (this is exciting) Linux apps (through container).

## Buy a Chromebook or Pixelbook
You do not need to do dirty hacks like turn on `developer` mode, install `crouton` or `termux`, or `dual boot` it with linux.
ChromeOS is very secure and it is one of its biggest advantages. Do not turn on the `developer` mode, which sacrifices its security.

## Turn on Linux (Beta)
ChromeOS has a built-in solution by hosting a `container` in a `linux vm`.

- Update your ChromeOS
    - Simply restart your laptop to check and update its OS.
- ~~Switch to `dev` channel~~
    - ~~https://support.google.com/chromebook/answer/1086915~~
- In Chrome browser address bar type [chrome://settings](chrome://settings), scroll down to Linux (Beta) and turn it on.

For now, it is a `debian stretch` but in future you can install any `linux`.

## Open `Terminal` and test
Hit Launcher (circle icon on bottom left of your desktop), search for  `terminal` and open it.

It is a fresh, clean, true `Debian GNU/Linux` in a container on an attached vm.
We are going to install our developing environment including `git`, `vscode`, `python` (miniconda), `gcloud sdk`.
These are inVisement choices. You can choose your dev portfolio apps.

```bash
sudo bash -c 'echo "deb http://http.us.debian.org/debian/ testing non-free contrib main" >> /atc/apt/sources.list'
sudo apt-get update
sudo apt-get install lsb-release
sudo apt-get install apt-transport-https
sudo apt-get install nano

# create a few folders
mkdir Downloads Docs PROJECTS Temp
cd Downloads
```

# Install `git` and clone repo
```bash
sudo git clone https://github.com/inVisement/HFaaS.git ~/PROJECTS/ #change repo address
```

## Install `vscode` or other ide/editor
```bash
curl -O https://vscode-update.azurewebsites.net/1.24.1/linux-deb-x64/stable
sudo apt ./code_*.deb
code
```

# Install `python`
```bash
# I recommend miniconda since conda package manager is better than pip to handle non python dependencies
curl -O https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh
sudo bash ./Miniconda*.deb # follow direction and choose directory ~/miniconda3
sudo conda install pandas
python3
print(5)
import pandas as pd
exit()
```

# Install `google cloud` sdk and set it up
```bash
export CLOUD_SDK_REPO="cloud-sdk-$(lsb_release -c -s)"
echo "deb https://packages.cloud.google.com/apt $CLOUD_SDK_REPO main" | sudo tee -a /etc/apt/sources.list.d/google-cloud-sdk.list
sudo apt-get update && sudo apt-get install google-cloud-sdk
sudo ap-get install google-cloud-sdk-app-engine-python
# you can install more components go to: https://cloud.google.com/sdk/docs/downloads-apt-get
gcloud iam service-accounts keys create MY_KEY_FILE.json --iam-account=<YOUR IAM ACCOUNT> # change it to yout iam account or download it through
gcloud auth activate-service-account --key-file=MY_KEY_FILE.json
gcloud init # follow instructions

```

## Pin `vscode, Files, Terminal` to desktop shelf
Hit Launcher (bottom left corner of desktop), search for desired app (i.e. vscode or Terminal or Files) right click by alt+click, and click `pin to shelf`.
Now, click on `vscode` on your destop shelf (bottom bar) to open it, it is beautiful (isn't it?!), write a little file, save it in PROJECTS.
PROJECTS.


## Enjoy and share
