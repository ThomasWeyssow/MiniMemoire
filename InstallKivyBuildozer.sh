#!/bin/bash

# pip3
sudo apt-get install python3-setuptools
sudo easy_install3 pip

# Kivy dependencies (necessary)
sudo apt-get install -y \
    build-essential \
    git \
    python3 \
    python3-dev \
    ffmpeg \
    libsdl2-dev \
    libsdl2-image-dev \
    libsdl2-mixer-dev \
    libsdl2-ttf-dev \
    libportmidi-dev \
    libswscale-dev \
    libavformat-dev \
    libavcodec-dev \
    zlib1g-dev

# Kivy dependencies (optional)
sudo apt-get install -y \
    libgstreamer1.0 \
    gstreamer1.0-plugins-base \
    gstreamer1.0-plugins-good \
    xclip \
    xsel

# Kivy
sudo -H pip3 install Cython==0.23
sudo -H pip3 install kivy

# Java
sudo apt-get install default-jdk
echo "JAVA_HOME=\"/usr/lib/jvm/java-8-openjdk-amd64\"" | sudo tee --append /etc/environment
source /etc/environment

# Buildozer
git clone https://github.com/kivy/buildozer
cd buildozer
python setup.py build
sudo -H pip3 install -e .
cd ..
sudo -H pip3 install --upgrade buildozer

# 32bit libraries
sudo dpkg --add-architecture i386
sudo apt-get update
sudo apt-get install -y \
    ccache \
    libncurses5:i386 \
    libstdc++6:i386 \
    libgtk2.0-0:i386 \
    libpangox-1.0-0:i386 \
    libpangoxft-1.0-0:i386 \
    libidn11:i386 \
    unzip \
    zlib1g:i386

# Buildozer dependencies (optional)
sudo apt-get install -y \
    automake \
    autoconf \
    libtool

# Extraire crystax-ndk-10.3.2-linux-x86_64.tar dans le répertoire 'Home'
# Effectuer le fix dans le fichier android.py: 
#     - https://github.com/kivy/buildozer/issues/613:
#     - (ou copier le fichier se trouvant dans le dossier MiniMemoire dans le dossier
#        ~/buildozer/buildozer/targets)
# Dans l'appareil Android: activer les options de développement -> autoriser le déboggage USB
# Débug Android: {adb kill-server; adb start-server; adb logcat -c; adb logcat; adb devices}

