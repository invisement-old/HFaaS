---
title: "Chromebook for Developers"
date: 2018-08-07
tags: ["Blog", "Chromebook", "Google Cloud", "Linux", "Pixelbook", "Crostini", "DevOps", "Python", "conda"]

---

<img src="images/vscode-chrome.png" width="100%">

ChromeOS is a modern approach to laptop: everything runs in a browser but it can host Linux apps. Now, there are serous high-end Chromebooks like Pixelbook from Google, Samsung, and Asus. Chromebooks are very secure, fast, beautiful, and functional. Now you can run Web apps (Dah!), Chrome apps and extensions, android apps (through google play), and (this is exciting) Linux apps (through hosted container).

## Buy a Chromebook or Pixelbook
You do not need to do dirty hacks like turn on `developer` mode, install `crouton` or `termux`, or `dual boot` it with linux.
ChromeOS is very secure and it is one of its biggest advantages. Do not turn on the `developer` mode, which sacrifices its security.

## Turn on Linux (Beta)
ChromeOS has a built-in solution by hosting a `container` in a `linux vm`.

- Update your ChromeOS
    - Simply restart your laptop to check and update its OS.
- Switch to `dev` or `beta` channel (after september 2018, this step is not necessary).
    - https://support.google.com/chromebook/answer/1086915
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
 #install a few good utils
sudo apt-get install lsb-release apt-transport-https nano wget

# create a few folders
mkdir Downloads Docs PROJECTS Temp PROJECTS/inVisement
cd Downloads
```

# Install `git` and clone repo
```bash
sudo install git
sudo git clone https://github.com/inVisement/HFaaS.git ~/PROJECTS/ #change repo address
git config --global user.name "your-user-name"
git config --global user.email "your-email"
```

Optionally, you can go to .git/config and edit url to add your usename (and password, but it is not secure though) like `url = https://your-username:your-password@the-repo-url-address`

# Install `python`
```bash
# I recommend miniconda since conda package manager is better than pip to handle non python dependencies
wget https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh
bash ./Miniconda* # follow direction.
# create virtual environment, activate it, install some packages, test it, deactivate it
conda create -n inVisement
cd ~/PROJECTS/inVisement
source activate inVisement
conda install numpy pandas
source deactivate
```


# Install `vscode` or other code editor
```bash
# download, install, open
wget -O vscode.deb https://go.microsoft.com/fwlink/?LinkID=760868 # or downloaded the file manually
sudo apt install ./vscode.deb
cd PROJECTS/inVisement
code # run vscode
```

In `vscode`, you can go to Extensions and install extensions you want like `python`, `go`, `docker`.

The change the default `python` interpreter to virtual environment. Press Ctr+Shift+P to launch command Pallete. Type `Python: Select Interpreter` and select it. Among your choices, choose "Anaconda Inc, Python whatever (your-env)".

Press Ctr+\` to toggle integrated terminal (or View > Integrated Terminal from Menue). 

Open your project folder (File > Open Folder) create a python file. Send any line or selection of lines to execute in terminal by Ctrl+Enter

Fortunately, `vscode` has an excellent `git` integration tool that you can find in sidebar icons to add and commit (check mark icon) and push and pull from the status bar. You can change repo and branch through status bar, too.


# Install `google cloud` sdk and set it up
```bash
export CLOUD_SDK_REPO="cloud-sdk-$(lsb_release -c -s)"
echo "deb https://packages.cloud.google.com/apt $CLOUD_SDK_REPO main" | sudo tee -a /etc/apt/sources.list.d/google-cloud-sdk.list
sudo apt-get update && sudo apt-get install google-cloud-sdk
sudo apt-get install google-cloud-sdk-app-engine-python
# you can install more components go to: https://cloud.google.com/sdk/docs/downloads-apt-get
gcloud init --concole-only # follow instructions. 
```

# install `hugo` static site generator
download the latest version from https://github.com/gohugoio/hugo/releases

```bash
wget https://github.com/gohugoio/hugo/releases/download/v0.46/hugo_0.46_Linux-64bit.deb
```




## Pin `vscode`, `Files`, `Terminal` to desktop shelf
Hit Launcher (bottom left corner of desktop), search for desired app (i.e. vscode or Terminal or Files) right click by alt+click, and click `pin to shelf`.
Now, click on `vscode` on your destop shelf (bottom bar) to open it, it is beautiful (isn't it?!), write a little file, save it in PROJECTS.
PROJECTS.


## Enjoy coding and share it, please
