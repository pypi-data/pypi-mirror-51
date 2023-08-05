### python-sdk for VisionSeed - a camera module with AI ability

# install
```shell
pip3 install visionseed
```

# run example
```shell
pip3 install opencv-python
pip3 install matplotlib
pip3 install cocos2d
python3 example/example.py
```

# run example on Windows
You need to modify the line in example.py, and replace "/dev/ttyACM0" to your VisionSeed's virtual port number, e.g. "COM3":
```python
datalink = vs.YtDataLink( serial.Serial("/dev/ttyACM0",115200,timeout=0.5) )
```

# more
Homepage: https://visionseed.youtu.qq.com
