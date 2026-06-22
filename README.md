


Build:
```
docker build -t piper-api .
```

Tải voice:
```
mkdir -p voices/en_US-lessac-medium

curl -L -o voices/en_US-lessac-medium/en_US-lessac-medium.onnx \
  https://huggingface.co/rhasspy/piper-voices/resolve/main/en/en_US/lessac/medium/en_US-lessac-medium.onnx

curl -L -o voices/en_US-lessac-medium/en_US-lessac-medium.onnx.json \
  https://huggingface.co/rhasspy/piper-voices/resolve/main/en/en_US/lessac/medium/en_US-lessac-medium.onnx.json
```

Run server:
```
docker run -d \
  --name piper-api \
  -p 9000:9000 \
  -v "$PWD/voices:/voices" \
  piper-api
```

Test:
```
curl -X POST http://127.0.0.1:9000/tts \
  -H "Content-Type: application/json" \
  -d '{"text":"Hello, this is a Piper API test."}' \
  --output test.wav
```

Gợi ý voice tiếng Anh
```
en_US-lessac-medium  
en_US-amy-medium  
en_US-ryan-medium
en_GB-alba-medium
```


https://piper.ttstool.com/   
https://rhasspy.github.io/piper-samples/#vi_VN-vais1000-medium


Test mặc định tiếng Anh:
```
curl -X POST http://127.0.0.1:9000/tts \
  -H "Content-Type: application/json" \
  -d '{"text":"Hello, this is the default English voice."}' \
  --output test_en.wav
```
  
  Test truyền model:
```
  curl -X POST http://127.0.0.1:9000/tts \
  -H "Content-Type: application/json" \
  -d '{"text":"Hello, this is English.", "model":"en"}' \
  --output test_en.wav
```
  
  Hoặc dùng voice:
```
  curl -X POST http://127.0.0.1:9000/tts \
  -H "Content-Type: application/json" \
  -d '{"text":"Hello, this is English.", "voice":"english"}' \
  --output test_english.wav
```  
  
  Nếu sau này có model tiếng Việt, thêm vào MODELS:
```
  "vi": "/voices/vi_VN-yourvoice/vi_VN-yourvoice.onnx",
"vietnamese": "/voices/vi_VN-yourvoice/vi_VN-yourvoice.onnx",
```
Rồi gọi:
```
curl -X POST http://127.0.0.1:9000/tts \
  -H "Content-Type: application/json" \
  -d '{"text":"Xin chào, đây là giọng tiếng Việt.", "model":"vi"}' \
  --output test_vi.wav
```  
  
Gitbash
Change app.py
1. Rebuild image
```
docker build -t piper-api .
```

2. Stop container cũ
```
docker rm -f piper-api
```

3. Run lại container
```
docker run -d \
  --name piper-api \
  -p 9000:9000 \
  -v "$(pwd -W)/voices:/voices" \
  -v "$(pwd -W)/app.py:/app/app.py" \
  piper-api

docker run -d --name piper-api -p 9000:9000 -v "$(pwd -W)/voices:/voices" -v "$(pwd -W)/app.py:/app/app.py" piper-api
```  
  
  4. Xem log
```
 docker logs -f piper-api
```

Sau này sửa app.py chỉ cần:
```
docker restart piper-api
```
các file voices
Test container thấy file chưa:
```
winpty docker exec -it piper-api sh
ls -lh /voices
```

<img src="/test/pic/1.jpg">
<img src="/test/pic/2.jpg">
<img src="/test/pic/3.png">
