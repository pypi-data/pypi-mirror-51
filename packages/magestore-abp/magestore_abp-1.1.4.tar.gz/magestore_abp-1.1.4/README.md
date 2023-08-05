## About
This package provided function *build_package* for build 6 Magestore product lines

## Prerequisite
Config local machine to run sudo without password
```bash
sudo visudo
# add this line to end of file
# <username> is your current username
<username>  ALL=(ALL) NOPASSWD: ALL
```
## How to use
1. Import function to your python file
```python
from magestore_abp import build_package
```
2.Function *build_package* will have required parameters
<ul>
  <li>repo_info: (type:dict)
        <ul>
            <li>repo_name: (type:str)</li>
            <li>repo_owner: (type:str)</li>
            <li>tag_name: (type:str)</li>
            <li>access_token: (type:str) personal access token to github that have permission to access to 6 Magestore product lines</li>
        </ul>
    </li>
</ul>
Execute this function and it will return local path to built package file on the local machine if build process successful, else return ''