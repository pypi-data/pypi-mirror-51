# X2Paddle
[![License](https://img.shields.io/badge/license-Apache%202-blue.svg)](LICENSE)
[![Version](https://img.shields.io/github/release/PaddlePaddle/X2Paddle.svg)](https://github.com/PaddlePaddle/X2Paddle/releases)  
X2Paddle支持将其余深度学习框架训练得到的模型，转换至PaddlePaddle模型。  
X2Paddle is a toolkit for converting trained model to PaddlePaddle from other deep learning frameworks.

## 更新历史
2019.08.05  
1. 统一tensorflow/caffe/onnx模型转换代码和对外接口
2. 解决上一版caffe2fluid无法转换多分支模型的问题
3. 解决Windows上保存模型无法加载的问题
4. 新增optimizer，优化代码结构，合并conv、batch_norm的bias和激活函数  

**如果你需要之前版本的tensorflow2fluid/caffe2fluid/onnx2fluid，可以继续访问release-0.3分支，获取之前版本的代码使用。**

## 环境依赖

python >= 3.5  
paddlepaddle >= 1.5.0  

**以下依赖只需对应安装自己需要的即可**  
转换tensorflow模型 ： tensorflow == 1.14.0  
转换caffe模型 ： caffe == 1.0.0  
转换onnx模型 ： onnx == 1.5.0  pytorch == 1.1.0
## 安装
### 安装方式一（推荐）
使用最新的代码版本，可使用如下方式进行安装  
```
pip install git+https://github.com/PaddlePaddle/X2Paddle.git@develop
```

### 安装方式二
我们会定期更新pip源上的x2paddle版本
```
pip install x2paddle
```

### 安装方式三
```
git clone https://github.com/PaddlePaddle/X2Paddle.git
cd X2Paddle
git checkout develop
python setup.py install
```

## 使用方法
### TensorFlow
```
x2paddle --framework=tensorflow --model=tf_model.pb --save_dir=pd_model
```
### Caffe
```
x2paddle --framework=caffe --prototxt=deploy.proto --weight=deploy.caffemodel --save_dir=pd_model
```
### ONNX
```
x2paddle --framework=onnx --model=onnx_model.onnx --save_dir=pd_model
```
### 参数选项
| 参数 | |
|----------|--------------|
|--framework | 源模型类型 (tensorflow、caffe、onnx) |
|--prototxt | 当framework为caffe时，该参数指定caffe模型的proto文件路径 |
|--weight | 当framework为caffe时，该参数指定caffe模型的参数文件路径 |
|--save_dir | 指定转换后的模型保存目录路径 |
|--model | 当framework为tensorflow/pmmx时，该参数指定tensorflow的pb模型文件或onnx模型路径 |
|--caffe_proto | [可选]由caffe.proto编译成caffe_pb2.py文件的存放路径，当存在自定义Layer时使用，默认为None |

## 使用转换后的模型
转换后的模型包括`model_with_code`和`inference_model`两个目录。  
`model_with_code`中保存了模型参数，和转换后的python模型代码  
`inference_model`中保存了序列化的模型结构和参数，可直接使用paddle的接口进行加载，见[load_inference_model](https://www.paddlepaddle.org.cn/documentation/docs/zh/1.5/api_guides/low_level/inference.html#api-guide-inference)

## 相关文档
1. [X2Paddle使用过程中常见问题](FAQ.md)  
2. [如何导出TensorFlow的pb模型](export_tf_model.md)
3. [X2Paddle测试模型库](x2paddle_model_zoo.md)


## Acknowledgements

X2Paddle refers to the following projects:
- [MMdnn](https://github.com/microsoft/MMdnn)
