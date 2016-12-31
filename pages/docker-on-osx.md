title: Running Docker on OSX
date: 2017-01-01
topic: DOCKER
intro: In this post, I'll cover the best way I've found to run Docker in my local OSX development environment.

This post won't cover what Docker is, or why you should use. That has been covered in more detail, better than I could here.

### Why not Docker For Mac?

Before we dive into the setup instruction, it's worth addressing, why not to use Docker's own recommended solution, Docker For Mac.
In short the file system. The current implementation of the file system results in high CPU usage when syncing (sharing) volumes.

As project's grow to include hundreds of files, the resulting slow down and strain becomes un-usable. Front end build processes that should be sub-second take up to a minute. Web servers reloading on file changes timeout. Tests run magnitudes slower then they should.

While, hopefully one day Docker For Mac's filesystem performance issues will be resolved, until then this is the most reliable and preformant I've found to run Docker on OSX.

### Step 1. Install Docker Toolbox

Download the `.pkg` from https://github.com/docker/toolbox/releases/tag/v1.12.3 and follow the GUI's install steps.

This will ensure the following packages are installed...
* VirtualBox
* Docker (client)
* Docker Compose
* Docker Machine

Once you've run through, you can optionally ensure all packages are present with a simple version check in the Terminal.

```
$ docker --version
Docker version 1.12.3, build 6b644ec
$ docker-machine --version
docker-machine version 0.8.2, build e18a919
$ docker-compose --version
docker-compose version 1.8.1, build 878cff1
```

### Step 2. Create a boot2docker VM with Docker Machine

Modify the command below according to your computer's specs. Once assigned, you cannot modify these settings without destroying then re-creating the VM.

Here are the two choices to make.

* `--virtualbox-memory` - How much memory (in MBs) you want to allow the VM. `4096` (or ~4GB) should be the absolute minimum. Typically you want to use half of your computer's memory.
* `--virtualbox-disk-size` - The maximum size (in MBs) allowed for the VM's disk size. `30000` (or ~30GB) is a good choice (you generally don't want to go below that).

With those values chosen, modify then run the following command...

```
docker-machine create -d virtualbox \
    --virtualbox-boot2docker-url=https://github.com/boot2docker/boot2docker/releases/download/v1.12.3/boot2docker.iso default \
    --virtualbox-memory "4096" \
    --virtualbox-disk-size "30000"
```

### Step 3. Enabling NFS

By default, the VM created shares your `/Users/` folders.
In order to use NFS on your freshly created VM, you'll need to install a 3rd party tool, called [`docker-machine-nfs`](https://github.com/adlogix/docker-machine-nfs).

You have two installation options, either curl or via brew. Your choice.

```
curl https://raw.githubusercontent.com/adlogix/docker-machine-nfs/master/docker-machine-nfs.sh | sudo tee /usr/local/bin/docker-machine-nfs > /dev/null && \
    sudo chmod +x /usr/local/bin/docker-machine-nfs
```

or

```
brew install docker-machine-nfs
```

Next, we'll mount the NFS drive to our machine, modify the command below according to your setup.

* `--shared-folder` - You want to set this to the absolute path of your development folder. If possible, limit this just where your code lives. This will result in significant higher performance, as less files need to be watched and synced to the VM.

With the folder choose, modify then run the following command...
```
docker-machine-nfs default \
    --mount-opts="noacl,async,nolock,vers=3,udp,noatime,actimeo=2" \
    --shared-folder="/Users/cameronmaske/Development/repos"
```

The `mount-opts` settings ensure any watch file changes play nicely with any front end builders.

### Step 4. Start the VM.

In order to run docker, you'll need to two things.
* Start the VM
* Set the env to your local terminal.

This requires running the following commands...

```
$ docker-machine start default
$ eval $(docker-machine env default)
```

I use ZSH as my shell. My normal workflow involves running `dm-up` to boot the VM and set env vars. Any other terminals opened check if the VM is running and if so run set up the env vars automatically.

In `.zshrc`
```
alias dm-up="docker-machine start default; eval '$(docker-machine env default)'"
alias dm-stop="docker-machine stop default"
```

### Step 5. Setting up `localdocker`.

With the VM running, run `docker-machine ip default` and note down the IP (mine is `192.168.99.100`).
For convenience, I like to setup the host alias `localdocker` to use instead of the IP.  

Open `/etc/hosts` with your terminal of choice (will need sudo access).

Add the following line.
```
192.168.99.100 localdocker
```

### Congratulations!

You've done it! You are now running Docker on OSX.
As a quick check run `docker ps` to verify everything is working. You should see the following.

### Benchmarks.

[TODO]
