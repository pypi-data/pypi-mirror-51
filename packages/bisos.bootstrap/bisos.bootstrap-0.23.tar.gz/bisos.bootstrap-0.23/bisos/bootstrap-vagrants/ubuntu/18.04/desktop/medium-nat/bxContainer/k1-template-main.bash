      cat  << _EOF_
 ######### PHASE 0: Parameters Specification
_EOF_
      genesisUserName=$(id -u -n)
      genesisUserGroup=$(id -g -n)
      genesisUserPasswd=vagrant
      bashPath=$(which bash)
      bxBootstrapBase="/var/bxBootstrap"
      
      genesisGitRepoCloneCmnd="{sysProvisionerObtain}"
      genesisGitRepoEntryCmnd="{sysProvisionerRun}"

      cat  << _EOF_
 ######### PAHSE 1: Create bxgenesis User -- Running As Root
_EOF_

      # sudo useradd bisos
      # echo $genesisUserPasswd | sudo -S passwd bisos --stdin
      # echo $genesisUserPasswd | sudo -S passwd root --stdin
      # sudo usermod -aG wheel bisos
      # sudo echo 'bisos ALL=(ALL) NOPASSWD: ALL' >> /etc/sudoers
      
      sudo apt-get -y  install git

      sudo mkdir -p $bxBootstrapBase
      sudo chown $genesisUserName:$genesisUserGroup $bxBootstrapBase

      cat  << _EOF_
 ######### PHASE 2: Bring Over genesisClone -- Running As $genesisUserName
_EOF_

      (set -x; id)
      
      sudo -u $genesisUserName $bashPath << _EOF_genessisUserName_

      (set -x; id)

      (set -x; git init)

      (set -x; mkdir -p $bxBootstrapBase/gitRepos)
      ls -ld $bxBootstrapBase/gitRepos

      ( set -x; cd $bxBootstrapBase/gitRepos; $genesisGitRepoCloneCmnd )

      ( set -x; cd $bxBootstrapBase/gitRepos; $genesisGitRepoEntryCmnd )

_EOF_genessisUserName_

      set -x
      id
      
      sudo -H pip install --no-cache-dir --upgrade pip
      sudo -H pip install --no-cache-dir --upgrade virtualenv
      sudo -H pip install --no-cache-dir --upgrade bisos.bx-bases

      sudo -H pip list
      set +x

      id

      cat  << _EOF_
 ######### PHASE 3: Cleanup and Shutdown  -- Running As Root
_EOF_
      
      #shutdown now
      #exit 0
