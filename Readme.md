# Send video to jinglepings

install dependancies
```bash
sudo apt update
sudo apt install python3 python3-pip libav-tools
pip3 install -r requirements.txt
```
preprocess video
```bash
chmod u+x prepreocess_video.sh 
./prepreocess_video.sh [my_video.mp4] [framerate]
```

```bash
sudo python3 test.py -i output -s 16x16 -n 100 -r 1 -I
```