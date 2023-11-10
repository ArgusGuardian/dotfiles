#!/bin/bash

set -e  # Exit on error
set -o pipefail  # Exit on command failure in a pipelines

# Function to check if a package is installed
function is_installed {
    if ! command -v $1 &> /dev/null; then
        return 1
    else
        return 0
    fi
}

# Function to install a package if it's not already installed
function install_package {
    if is_installed $1; then
        echo "$1 is already installed."
    else
        echo "Installing $1..."
        sudo dnf install -y $1
    fi
}

# Function to add a repository
function add_repo {
    repo_url=$1
    repo_key=$2

    if sudo dnf config-manager --query -- "$repo_url"; then
        echo "Repository $repo_url already exists."
    else
        echo "Adding repository $repo_url..."
        sudo dnf config-manager --add-repo $repo_url
        sudo rpm --import $repo_key
    fi
}

# Update the system
echo "updating the system\n"
sudo dnf update
echo "system updated\n"
# Add repositories
add_repo https://brave-browser-rpm-release.s3.brave.com/brave-browser.repo https://brave-browser-rpm-release.s3.brave.com/brave-core.asc
dnf copr enable frostyx/qtile

# Install essentials
packages=(
    rofi newsboat unzip lxappearance qt5ct nitrogen sxhkd picom qtile qtile-extras dunst network-manager-applet xfce4-power-manager numlockx blueman polkit-gnome xfce4-notifyd xfce4-notifyd volumeicon kitty ranger brave-browser bleachbit btop mpv flameshot geany neofetch thunar catfish eog gnome-disk-utility celluloid timeshift xfce4-terminal git curl neovim python3-neovim
)

echo "installing packages\n"
for package in "${packages[@]}"; do
    install_package $package
done
echo "packages installed\n"
# Download and install nerdfont
nerd_font_url="https://github.com/ryanoasis/nerd-fonts/releases/download/v3.0.2/IosevkaTerm.zip"
nerd_font_dir="/home/alaa/.local/share/fonts"

echo "Downloading and installing Nerd Font...\n"
wget $nerd_font_url
mkdir -p $nerd_font_dir
unzip IosevkaTerm.zip -d $nerd_font_dir
fc-cache -fv

echo "fonts installed\n"

# theming terminal 
echo "Setting up terminal theme...\n"
git clone https://github.com/ChrisTitusTech/mybash.git
cd mybash
./setup.sh
echo "Terminal theme setup complete.\n"

# installing nvchad
echo "installing nvchad...\n"
git clone https://github.com/NvChad/NvChad ~/.config/nvim --depth 1

# Copy configuration files
config_files=(
    .bashrc
    .bash_profile
    .config
    .icons
    .themes
    .gtkrc-2.0
    .newsboat
)

for file in "${config_files[@]}"; do
    cp -r $file $HOME/
done

cp rofi/rofi-power-menu $HOME/.local/bin/
cp -r rofi/rofi $HOME/.local/share/


echo "Setup complete!\n"
echo "run neovim to complete the nvchad installation\n"
nvim
