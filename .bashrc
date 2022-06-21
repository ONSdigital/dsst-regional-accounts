export HOME=$PWD

# This determines the current branch name for a git repo when a git directory is navigated to
function git-current-branch-name {
  git symbolic-ref HEAD 2>/dev/null | cut -d"/" -f 3,4

}

# This adds a variable to display the current branch name in the command prompt
function git-branch-prompt {
  local branch=`git-current-branch-name`
  if [ $branch ]; then printf " [%s]" $branch; fi
}

# This adds a variable to display how many commits behind/ahead the current branch is in the command prompt
function git-commit-behind-ahead {
  commit_behind=''
  local current_branch=`git-current-branch-name`
  if [[ -n $current_branch ]]; then
    current_remote=$(git config branch.$current_branch.remote);
    current_merge_branch=$(git config branch.$current_branch.merge | cut -d / -f 3,4);

    if [[ -n $current_merge_branch ]]; then
      commit_behind=$(git rev-list --left-only --count $current_remote/$current_merge_branch...$current_branch);
      commit_ahead=$(git rev-list --right-only --count $current_remote/$current_merge_branch...$current_branch);
    fi

  fi

  if [ $commit_behind ]; then printf "[\001\e[1;31m\002%s\001\e[0m\002|\001\e[1;32m\002%s\001\e[0m\002]" $commit_behind $commit_ahead;  fi
}

# This defines the prompt display in the terminal of the form:
# me: current_dir [current_branch][commits behind|commits ahead]:
PS1="\[\033[0;36m\]\w\[\033[0m\]\[\033[0;33m\]\$(git-branch-prompt)\[\033[0m\]\$(git-commit-behind-ahead):"

# Bring colour to the ls command
alias ls='ls --color=auto'
LS_COLORS='di=0;31:fi=0:ex=0;32'
export LS_COLORS

# Start typing the command then tap up or down to search bash history.
bind '"\e[A": history-search-backward'
bind '"\e[B": history-search-forward'
bind '"\eOA": history-search-backward'
bind '"\eOB": history-search-forward'

### Aliases

# Aliases for installing new packages.
alias pi='pip install'
alias pu='pip install -U'
alias ci='conda install -y'
alias cu='conda update -y'
alias pup='python -m pip install -U pip'

# Useful git aliases - modify at your pleasure.
alias gs='git status'
alias ga='git add'
alias grs='git restore --staged'
alias gb='git branch'
alias gbm='gb -m'
__git_complete gbm _git_branch
alias gbd='gb -d'
__git_complete gbd _git_branch
alias gc='git commit'
alias gca='gcsmsg --amend'
alias gcaf='gcsmsg --amend --no-edit'
alias gcsaf='SKIP=flake8 gc --amend --no-edit'
alias gcs='SKIP=flake8 git commit'
alias gcsf='SKIP=flake8 git commit'
alias gd='git diff'
alias gds='git diff --staged'
alias gco='git checkout'
__git_complete gco _git_checkout
alias gcb='git checkout -b'
__git_complete gcb _git_checkout
alias gp='git push'
alias gpft='gp --follow-tags'
alias gpu='git push -u origin HEAD'
alias gf='git fetch'
alias gpl='git pull'
alias grh='git reset HEAD'
alias gsl='git stash list'
alias gspu='git stash push -m'
# Removes all merged branches locally.
alias tidygit="git checkout master && git branch --merged | egrep -v '(^\*|master)' | xargs git branch -d && git remote prune origin"

# Stash functions.
# Pass a number to pop the stash at that position.
gspo() {
  if [ $# -eq 0 ]; then
    git stash pop
  else
    git stash pop stash@{$1}
  fi
}
# Drop stash at position.
gsd() {
  git stash drop stash@{$1}
}
# Show stash at position.
gss() {
  git show stash@{$1}
}
