---
title: "Chromebook for Developers"
date: 2018-08-01
tags: ["Blog", "Chromebook", "Google Cloud", "Linux", "Pixelbook", "Crostini", "DevOps", "Python", "conda"]
card: '<img src="/images/vscode-chrome.png" width="100%">'

---

ChromeOS is a modern approach to laptop: everything runs in a browser but it can host Android and Linux apps. 

You can run Web apps (Dah!), Chrome apps and extensions, android apps (through google play), and (this is exciting) Linux apps (through hosted container). You do not need to do dirty hacks like turn on `developer` mode, install `crouton` or `termux`, or `dual boot` it with linux.

Chromebooks are very secure, fast, beautiful, and functional. Mine is a Pixelbook and it is the best device I ever had. 

## Turn on Linux (Beta)
ChromeOS has a built-in solution by hosting a `container` in a `linux vm`.

- Update your ChromeOS
    - Simply restart your laptop to check and update its OS.
- Switch to `dev` or `beta` channel (after september 2018, this step is not necessary).
    - https://support.google.com/chromebook/answer/1086915
- In Chrome browser address bar type [chrome://settings](chrome://settings), scroll down to Linux (Beta) and turn it on.

For now, it is a `debian stretch` but in future you can install any `linux`.

## Open Terminal and test
Hit Launcher (circle icon on bottom left of your desktop), search for  `terminal` and open it.

It is a fresh, clean, true `Debian GNU/Linux` in a container on an attached vm.
We are going to install our developing environment including `git`, `vscode`, `python` (miniconda), `gcloud sdk`.
These are inVisement choices. You can choose your dev portfolio apps.

```bash
sudo bash -c 'echo "deb http://http.us.debian.org/debian/ testing non-free contrib main" >> /etc/apt/sources.list'
sudo apt-get update
 #install a few good utils
sudo apt-get install lsb-release apt-transport-https nano wget

# create a few folders
mkdir Downloads Docs PROJECTS Temp PROJECTS/inVisement
cd Downloads
```

## Install git and clone repo
```bash
sudo apt-get install git
git clone https://your-repo-address your-local-repo-folder #change repo address like
#git clone https://github.com/inVisement/HFaaS.git ~/PROJECTS/inVisement
git config --global user.name "your-user-name"
git config --global user.email "your-email"
```

Optionally, you can go to .git/config and edit url to add your usename (and password, but it is not secure though) like `url = https://your-username:your-password@the-repo-url-address` so push and pull will no longer needs yousername and password.

You may also change `.git/info/exclude` file to exclude some files and folder that you do not want git track them (like personal and hidden folders) to not clutter the repo.

## Install chromium, conda, python, vscode, etc.

```bash
sudo apt-get install chromium
```

You will see that chromium browser (in blue colors) is installed and its icon is pinned to your shelf by default (sweet). This is chromium browser that runs inside your Linux `terminal` and is different google chrome which runs on your chrome os directly.

You can download any `.deb` debian package in your `Linux` folders and double click on it to install it, another sweet feature of chrome os. Let us download `vscode` and `Anaconda` and install them: just google them in `chromium`, download their file, double click, and install.

If you and like me and prefer `miniconda` instead of `anaconda`, do this: 

```bash
# I recommend miniconda or anaconda since conda package manager is better than pip to handle non python dependencies
wget https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh
bash ./Miniconda* # follow instruction. or bash./Anaconda*
```

## Pin applications to desktop shelf
Usually chrome os pins linux application that has graphical ui to the shelf automatically. But in case you want to do you yourself, Hit Launcher (bottom left corner of desktop), search for desired app (i.e. vscode or Terminal or Files) right click by alt+click, and click `pin to shelf`. To launch any linux app either hot the icon, or search it in Launcher (that left-bottom circle), or type it in `termical`.


## Creating IDE to code
Launch `code` (vscode), open your project folder (File>Open Folder), toggle its integrated `terminal` (View>Terminal or ctrl+\`). 

In `vscode`, you can go to Extensions (left side bar or Ctrl+Shift+X) and install extensions you want like `python`, `go`, `docker`, hit reload to reload vscode.

Let us create and activate a python virtual environment. In `Terminal` (of `vscode`) type:

```bash
# create virtual environment, activate it, install some packages, test it, deactivate it
conda create -n inVisement
source activate inVisement
conda install numpy pandas pip # install a few packages that you want
source deactivate
```

The change the default `python` interpreter to virtual environment. Press Ctr+Shift+P to launch command Pallete. Type `Python: Select Interpreter` and select it. Among your choices, choose "Anaconda Inc, Python whatever (your-env)".

Open your project folder (File > Open Folder) and create a python file. Send any line or selection of lines to execute in terminal by Ctrl+Enter.

Fortunately, `vscode` has an excellent `git` integration tool that you can find in sidebar icons to add and commit (check mark icon) and push and pull from the status bar. You can change repo and branch through status bar, too.

Congratulation, you are coding from chrome os and it is so convenient and beautiful.

## Install cloud sdk and set it up

Follow instructions here in google page:
https://cloud.google.com/sdk/docs/quickstart-debian-ubuntu
Just do not forget that `gcloud init` might start authonticating on your chrome os browser, just copy that link to your linux chromium browser so container understands who you are or do `gloud init --console-only` and follow instructions. 

```bash
# Create environment variable for correct distribution
export CLOUD_SDK_REPO="cloud-sdk-$(lsb_release -c -s)"

# Add the Cloud SDK distribution URI as a package source
echo "deb http://packages.cloud.google.com/apt $CLOUD_SDK_REPO main" | sudo tee -a /etc/apt/sources.list.d/google-cloud-sdk.list

# Import the Google Cloud Platform public key
curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo apt-key add -

# Update the package list and install the Cloud SDK
sudo apt-get update && sudo apt-get install google-cloud-sdk

# Install some coud components lile python app engine
sudo apt-get install google-cloud-sdk-app-engine-python
# you can install more components go to: https://cloud.google.com/sdk/docs/downloads-apt-get

gcloud init --concole-only # follow instructions. 
```

## Enjoy coding and share it
Chrome OS is developing very fast and becomming an exciting project. Our organization is fully moved to google platform (for cloud, os, gmail, g suite, etc.) and I believe google offers very young but excellent working platform.
