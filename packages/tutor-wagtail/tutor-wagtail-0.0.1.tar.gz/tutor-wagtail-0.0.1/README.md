## tutor wagtail 插件。

wagtail docker化， 使用tutor插件实现wagtail本地部署和集群部署。

参考文档： https://docs.tutor.overhang.io/plugins.html

安装插件

    pip install -e .

开启插件：

    tutor plugins enable wagtail
 
保存配置：

    tutor config save 

通过插件Dockerfile来build images： 

    hooks = {
        "build-image": {"myimage": "myimage:latest"}
    }
    
使用此钩子，用户将能够myimage:latest通过运行以下命令来构建docker镜像：

    tutor images build wagtail
    
如何推送images到dockerhub:

    hooks = {
    "remote-image": {"myimage": "myimage:latest"},
}

使用此钩子，用户可以myimage:latest通过运行以下方式来推送到dockerhub(需要docker login)：
  
    tutor images push wagtail

最后执行命令：

    tutor local quickstart
    tutor config save --set K8S_NAMESPACE="yournamespace"
    tutor k8s quickstart



