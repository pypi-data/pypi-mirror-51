# rscli

Reckonsys CLI toolchain

## Who is this for?

`rscli` is an internal toolchain that we use here at Reckonsys to manage our workflows. If you are not an employee at Reckonsys, this tool may not make any sense to you.


## What will it do?

* Scaffolds out project
* Adds `.gitginore`
* Adds `.version.json`
* Adds `guniconfig.py` (For python projects)
* Adds `yarn build:<env>` (For node projects)

## Completion

### Bash

Add the following line in your `.bashrc` or `.bash_profile`

```
source <(rscli --print-completion-script bash)
```

### zsh

```
source <(rscli --print-completion-script zsh)
```

### fish

```
source <(rscli --print-completion-script fish)
```
