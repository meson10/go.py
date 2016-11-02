# go.py
A shim/wrapper for Go commands to make workspace level gopaths easier.

So you have a workspace.

$HOME
  /workspace
    /<org1>
       /repo1
       /repo2
    /<org2>
      /repo1
      /repo2
    
You do not want to share a common GoPath among them and rather have a gopath unique to both.
Easy, just create a directory called `gopath` inside /org1 and /org2. And build/run/compile using go.py

Example Usage:


Build a project:

```
meson10@xps:~/workspace/client1/project$ go.py go build .
Setting GOPATH to /home/meson10/workspace/client1/gopath
$:
```

Installing dependencies.
```
meson10@xps:~/workspace/client1/project$ go.py go get github.com/tools/godep
Setting GOPATH to /home/meson10/workspace/client1/gopath
$:
```

Running other binaries (Picks up godep installed at /home/meson10/workspace/client1/gopath/bin/)

```
meson10@xps:~/workspace/client1/project$ go.py godep restore .
Setting GOPATH to /home/meson10/workspace/client1/gopath
$:
```
