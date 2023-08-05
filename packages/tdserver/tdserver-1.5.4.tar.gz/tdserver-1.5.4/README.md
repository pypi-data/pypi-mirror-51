# tdserver使用说明

## 1. 服务部署
```python

from tdserver import BaseHandler, deploy


class DemoHandler(BaseHandler):
    def algorithm(self, req):
        """
        继承方法：定义你自己的处理方法
        获取图像：image = self.build_image(req) 内部调用返回numpy image 
        染回参数：请使用self.build_resp((True, str(req)))
        """
        return self.build_resp((True, str(req)))


if __name__ == '__main__':
    deploy(8080, DemoHandler)
```

## 2. 服务调用
```python

from tdserver import ImageServer


if __name__ == '__main__':
    # 通过服务地址构造服务
    d = ImageServer('http://0.0.0.0:8080/inference')
    # 传入参数字典参数idict（这里可以自定义传输）
    # 如果想传入图像文件，请使用idict = d.build_warpimg(image, idict)
    req = d.send({"a": 1, "b": "hello world!"})
    print(req)
```
