# ancora_get
Python script to download all CNE data from Ancora (https://ancora.genereg.net/)

Files will be downloaded as `gzip`, can unzip all (if needed) with something like `ls ./*/**/*.gz | parallel --max-args=1 -j12 gunzip {}`
