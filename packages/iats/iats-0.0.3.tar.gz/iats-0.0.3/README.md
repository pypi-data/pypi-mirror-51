# minimal ats kernel for jupyter

### goals:
 * Teaching ats
 * Sharing source code
 * Make ats available to a larger audience.
 * With the existence of [Google Colab](https://colab.research.google.com/), [mybinder](https://mybinder.org/) and the like we can distribute interactive notebooks using the ats kernel through a web browser.

![Example colab notebook](extra/img/colab_example.png?raw=true "Example of notebook")

Try out [ATS in Google Colaboratory](https://colab.research.google.com/drive/1cIpPX_6blrMQNa_RA9LMGIxhE23fWNYg)

## Manual installation

![Example of notebook](extra/img/example-notebook.png?raw=true "Example of notebook")

#### requirements:
  * gcc
  * python 3, pip, jupyter
  * ats-temptory

### steps:
 * pip install iats --user 
 * install_ats_kernel
 * `jupyter notebook`

### package
 * view online on pypi.org [here](https://pypi.org/project/iats/)

## for use with Docker
 * `docker pull telos/iats`
 * `docker run -p 8888:8888 telos/iats`
 * Copy the given URL containing the token, and browse to it. For instance:
 
 ```
 Copy/paste this URL into your browser when you connect for the first time,
 to login with a token:
    http://localhost:8888/?token=66750c80bd0788f6ba15760aadz53beb9a9fb4cf8ac15ce8
 ```
### editing

The docker image installs the kernel in editable mode, meaning that you can
change the code in real-time in Docker. For that, just run the docker box like
that:

```bash
git clone https://github.com/sparverius/iats.git
cd iats
docker run -v $(pwd):/jupyter/iats/ -p 8888:8888 sparverius/iats
```

This clones the source, run the kernel, and binds the current folder (the one
you just cloned) to the corresponding folder in Docker.
Now, if you change the source, it will be reflected in [http://localhost:8888](http://localhost:8888)
instantly. Do not forget to click "restart" the kernel on the page as it does
not auto-restart.

### in progress:
 * get ats kernel installed in a Google Colaboratory Notebook
 ![Example installing notebook](extra/img/colab_install.png?raw=true "Example of notebook")
 * syntax highlighting! (through codemirror)
 * many features available to program (i.e. code completion etc.)
