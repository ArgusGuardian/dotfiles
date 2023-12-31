#!/bin/bash

set -e          # Exit on error
set -o pipefail # Exit on command failure in a pipelines

# Function to check if a package is installed
function is_installed {
	if ! command -v $1 &>/dev/null; then
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

# get the username
read -p "Please enter the system username: " User
if [ -z "$User" ]; then
	echo "Error: Username cannot be empty. Exiting."
	exit 1
fi

# Update the system
echo "updating the system\n"
sudo dnf -y update
echo "system updated\n"

# Add repositories
#add_repo https://brave-browser-rpm-release.s3.brave.com/brave-browser.repo https://brave-browser-rpm-release.s3.brave.com/brave-core.asc
dnf copr enable frostyx/qtile

# Install essentials
packages=(
	rofi volumeicon light-locker newsboat unzip lxappearance qt5ct nitrogen sxhkd picom qtile qtile-extras dunst network-manager-applet xfce4-power-manager numlockx blueman xfce-polkit xfce4-notifyd xfce4-notifyd volumeicon kitty ranger brave-browser bleachbit btop mpv flameshot geany neofetch thunar catfish eog gnome-disk-utility celluloid timeshift xfce4-terminal git curl neovim python3-neovim variety imagemagick
)

echo "installing packages\n"
for package in "${packages[@]}"; do
	install_package $package
done
echo "packages installed\n"

# install pywall
sudo pip3 install pywal
# Download and install nerdfont
nerd_font_url="https://github.com/ryanoasis/nerd-fonts/releases/download/v3.0.2/IosevkaTerm.zip"
nerd_font_dir="/home/$User/.local/share/fonts"

echo "Downloading and installing Nerd Font...\n"
wget $nerd_font_url
mkdir -p $nerd_font_dir
unzip IosevkaTerm.zip -d $nerd_font_dir
fc-cache -fv
rm IosevkaTerm.zip

echo "fonts installed\n"

# theming terminal
echo "Setting up terminal theme...\n"
git clone https://github.com/ChrisTitusTech/mybash.git
cd mybash
./setup.sh
echo "Terminal theme setup complete.\n"
cd ..

# installing lazyvim
echo "installing lazyvim...\n"
git clone https://github.com/LazyVim/starter ~/.config/nvim
rm -rf ~/.config/nvim/.git

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
	sudo cp -r $file /home/$User/
done

sudo cp rofi/* /home/$User/.local/bin/

echo "Setup complete!\n"
echo "run neovim to complete the nvchad installation\n"
nvim
