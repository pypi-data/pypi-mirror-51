<!--
https://pypi.org/project/readme-generator/
https://pypi.org/project/python-readme-generator/
-->

[![](https://img.shields.io/badge/OS-Unix-blue.svg?longCache=True)]()

#### Installation
```bash
$ [sudo] pip install webpack-s3
```

#### Pros
+   store webpack build/etc files on S3

#### How it works
`webpack/` hard-coded folder

scripts:
+   create full-access/read-only user and credentials
+   upload/download `webpack/`

hard-coded environment variables names:
+   `AWS_S3_WEBPACK_BUCKET`
+   `AWS_S3_WEBPACK_USER`
+   `AWS_S3_WEBPACK_ACCESS_KEY_ID`
+   `AWS_S3_WEBPACK_SECRET_ACCESS_KEY`

webpack prod config:
```javascript
const output = {
  path: path.resolve('./webpack'),
  filename: "[name]-[hash].js",
  publicPath: 'https://'+process.env.AWS_S3_WEBPACK_BUCKET+'.s3.amazonaws.com/'
}
```

#### Scripts usage
command|`usage`
-|-
`webpack-s3` |`usage: webpack-s3 command [args]`
`webpack-s3-create-bucket` |`usage: webpack-s3-create-bucket bucket`
`webpack-s3-create-full-access-env` |`usage: webpack-s3-create-full-access-env bucket`
`webpack-s3-create-read-only-env` |`usage: webpack-s3-create-read-only-env bucket`
`webpack-s3-download` |`usage: webpack-s3-download`
`webpack-s3-upload` |`usage: webpack-s3-upload`

#### Examples
`Makefile`, create env
```bash
WEBPACK_BUCKET:=BUCKET_NAME
all:
    test -s .env.s3.webpack || webpack-s3-create-full-access-env $(WEBPACK_BUCKET) > .env.s3.webpack
    test -s .env.prod.webpack || webpack-s3-create-read-only-env $(WEBPACK_BUCKET) > .env.prod.webpack
```

build and upload to S3 
```bash
set -o allexport
. .env.s3.webpack || exit

webpack --config webpack.config.prod.js || exit
webpack-s3-upload
```

##### optional: deploy webpack files to server

`Dockerfile` 
```Dockerfile
ENTRYPOINT ["/bin/sh","/entrypoint.sh"]
```

`entrypoint.sh`
```bash
webpack-s3-download
...
```

`ansible-playbook.yml`
```yml
...
  tasks:
  - name: task_name
    docker_container:
      ...
      env_file: ".env"
```

<p align="center">
    <a href="https://pypi.org/project/python-readme-generator/">python-readme-generator</a>
</p>