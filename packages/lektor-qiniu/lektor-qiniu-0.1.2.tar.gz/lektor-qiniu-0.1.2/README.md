# lektor-qiniu  Lektor CMS 七牛云插件

lektor-qiniu is a plugin to deploy your lektor site to a qiniu cloud bucket.



## Main Features ##
1. deploy your site from Lektor admin dashboard to your qiniu bucket
2. deploy your site to folder in a qiniu bucket
3. exclude files and directories from deployment.
4. refresh your qiniu cdn.



## Before Installation ##

You may need a bucket from qiniu cloud to deploy your lektor project. Qiniu Cloud provides 10GB storage and cdn for free, that should be enough for most small projects.

Go to [`QINIU Cloud`](https://portal.qiniu.com/signup?code=1hltq2pevt7bm) for more details.

 **This plugin does not do anything to help you create or configure qiniu account or bucket.**  You will have to make it done by yourself. 


## Installation ##


There ways to install plugin in Lektor, the easy ways is run below command in your project.

```console
lektor plugins add lektor-qiniu
```

Press Enter and lektor will automatically download and install this plugin for you.


## Usage ##

After Installation, open your lektorproject file, first it should have a section like this:

```ini
[packages]
lektor-qiniu= 0.1.2
```

then below this section, you need add your bucket and folder(optional) as a target of a deploy server, like this:


```ini
[servers.qiniu]
name = qiniu
enabled = yes
target = qiniu://<YOUR-BUCKET>
```

or if you want deploy your site to a folder in a bucket, mostly for backups, you can add server section as below:

```ini
[servers.qiniu]
name = qiniu
enabled = yes
target = qiniu://<YOUR-BUCKET>/<NAME-OF-FOLDER>
```

for example, if you want to deploy your site to a bucket name "abcde", folder "fjhi", you will need to add a server section as below:

```ini
[servers.qiniu]
name = qiniu
enabled = yes
target = qiniu://abcde/fjhi
```


## Configuration ##

After setup your target server, you need to configure the plugin to make it works.

Go to your project's configs folder, which should be in root directory of your project. this folder is where Lektor keep the configuration files of all plugins. If you can't find any **configs** folder in your project's root directory, you need create it.

In configs folder, create a configuration file exactly named **qiniu.ini**.


#### Attention: DO NOT name the configuration file with other names, otherwise this plugin will not work properly.####


In this configuration file, you will need add few more sections, you can copy a sample configuration ini file from the sample_config folder, it looks like this:

```ini
[auth]
Access_Key = replace_with_your_own_AK
Secret_Key = replace_with_your_won_SK

[cdn]
refresh_enable =  yes
refresh_url = https://www.your-own-site.com/

[exclusions]
dirs = .lektor
files =  
```

You need to get your own Access Key and Secret Key from Qiniu Admin Dashboard, and put them in the **auth**  section.

mostly, Qiniu provides a free(with limitations) cdn for your bucket site, after you update your bucket file, the cdn wouldn't update automatically, therefore you will need to refresh your bucket site's directory (via your site's root url), for more details you can check Qiniu's documentation.

fortunately, you don't need to do refresh manually, you can just set the **refresh_enable** to **yes** in your **cdn** section, and change the refresh_url to your site's root url. this plugin will automatically refresh your cdn site after all files are uploaded.



