# curl -s http://server/path/script.sh | bash -s arg1 arg2

# cmd to install curl script
# curl https://raw.githubusercontent.com/DevAtDawn/openai_cli/main/codex_auto_edit/install.sh | bash

echo "curl install script"

# check if $HOME/bin exists
if [ ! -d "$HOME/bin" ]; then
    mkdir -p "$HOME/bin"
fi

# check if $HOME/bin is in $PATH

if [[ ":$PATH:" != *":$HOME/bin:"* ]]; then
    echo "export PATH=$HOME/bin:$PATH" >> ~/.bashrc
    export PATH="$HOME/bin:$PATH"
fi

# url to script
SCRIPT_URL="https://raw.githubusercontent.com/DevAtDawn/openai_cli/main/codex_auto_edit/codex_auto_edit.sh"
# script name is the last part of the URL
SCRIPT_NAME=$(basename "$SCRIPT_URL")

# download the script
curl -s $SCRIPT_URL -o "$HOME/bin/${SCRIPT_NAME}"

# verify the script
# if [ -f "$HOME/bin/${SCRIPT_NAME}" ]; then
    # chmod +x "$HOME/bin/${SCRIPT_NAME}"
    # echo "Downloaded $SCRIPT_NAME to $HOME/bin"
# else
    # echo "Failed to download $SCRIPT_NAME"
# fi

# make it executable
chmod +x "$HOME/bin/${SCRIPT_NAME}"

# run the script
# "$HOME/bin/${SCRIPT_NAME}" arg1 arg2
