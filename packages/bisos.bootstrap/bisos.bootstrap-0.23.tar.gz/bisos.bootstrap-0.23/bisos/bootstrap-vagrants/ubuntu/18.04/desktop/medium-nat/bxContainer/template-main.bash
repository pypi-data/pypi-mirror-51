      cat  << _EOF_
 ######### PHASE 0: Parameters Specification
_EOF_

      genesisUserName=$(id -u -n)
      if [ $genesisUserName == "root" ] ; then
	  genesisUserName="vagrant"
      fi
      genesisUserGroup=$(id -g -n)
      if [ $genesisUserGroup == "root" ] ; then
	  genesisUserGroup="vagrant"
      fi
      genesisUserPasswd=vagrant
      bashPath=$(which bash)
      bxBootstrapBase="/var/bxBootstrap"
      
      genesisGitRepoCloneCmnd="{sysProvisionerObtain}"
      genesisGitRepoEntryCmnd="{sysProvisionerRun}"

      cat  << _EOF_
 ######### PAHSE 1: Updating And Installing Distro Pkgs 
_EOF_

      set -x
      
      sudo apt-get update
      sudo apt-get -y install git      

      sudo mkdir -p $bxBootstrapBase
      sudo chown $genesisUserName:$genesisUserGroup $bxBootstrapBase

      cat  << _EOF_
 ######### PHASE 2: Bring Over genesisClone -- Running As $genesisUserName
_EOF_

      id

      sudo -u $genesisUserName id

      sudo -u $genesisUserName mkdir -p $bxBootstrapBase/gitRepos
      
      ls -ld $bxBootstrapBase/gitRepos

      sudo -u $genesisUserName -- sh -c  "cd $bxBootstrapBase/gitRepos; $genesisGitRepoCloneCmnd"

      sudo -u $genesisUserName -- sh -c  "cd $bxBootstrapBase/gitRepos; $genesisGitRepoEntryCmnd"

      
      
      cat  << _EOF_
 ######### PHASE 3: Cleanup and Shutdown  -- Running As Root
_EOF_
      
      #shutdown now
      #exit 0
