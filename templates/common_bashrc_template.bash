alias conda-update-and-clean="conda update --all -y && conda clean --all -y"
alias anvi-activate="conda activate anvio-master && source ~/.venvs/anvio-master/bin/activate"

alias ll="ls -ahlp"
alias vi=nvim
alias tmax="tmux attach"
alias vrsync="rsync -mahvP"
alias create_tar="tar -cf"
alias untar="tar -xf"

tarbz2() {
    create_tar "$1.tar.bz2" --use-compress-prog=pbzip2 "${@:2}"
}

untarbz2() {
    untar "$1" --use-compress-program="pbzip2 -d"
}

jup-remote() {
    ssh -NfL localhost:$1:localhost:$2 $3 && open http://localhost:$1
}
