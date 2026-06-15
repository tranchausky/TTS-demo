#!/usr/bin/env bash
set -e

mkdir -p voices/en_US-lessac-high
curl -L -o voices/en_US-lessac-high/en_US-lessac-high.onnx \
  https://huggingface.co/rhasspy/piper-voices/resolve/main/en/en_US/lessac/high/en_US-lessac-high.onnx
curl -L -o voices/en_US-lessac-high/en_US-lessac-high.onnx.json \
  https://huggingface.co/rhasspy/piper-voices/resolve/main/en/en_US/lessac/high/en_US-lessac-high.onnx.json

mkdir -p voices/en_US-lessac-medium
curl -L -o voices/en_US-lessac-medium/en_US-lessac-medium.onnx \
  https://huggingface.co/rhasspy/piper-voices/resolve/main/en/en_US/lessac/medium/en_US-lessac-medium.onnx
curl -L -o voices/en_US-lessac-medium/en_US-lessac-medium.onnx.json \
  https://huggingface.co/rhasspy/piper-voices/resolve/main/en/en_US/lessac/medium/en_US-lessac-medium.onnx.json

mkdir -p voices/en_US-amy-medium
curl -L -o voices/en_US-amy-medium/en_US-amy-medium.onnx \
  https://huggingface.co/rhasspy/piper-voices/resolve/main/en/en_US/amy/medium/en_US-amy-medium.onnx
curl -L -o voices/en_US-amy-medium/en_US-amy-medium.onnx.json \
  https://huggingface.co/rhasspy/piper-voices/resolve/main/en/en_US/amy/medium/en_US-amy-medium.onnx.json

mkdir -p voices/vi_VN-vais1000-medium
curl -L -o voices/vi_VN-vais1000-medium/vi_VN-vais1000-medium.onnx \
  https://huggingface.co/rhasspy/piper-voices/resolve/main/vi/vi_VN/vais1000/medium/vi_VN-vais1000-medium.onnx
curl -L -o voices/vi_VN-vais1000-medium/vi_VN-vais1000-medium.onnx.json \
  https://huggingface.co/rhasspy/piper-voices/resolve/main/vi/vi_VN/vais1000/medium/vi_VN-vais1000-medium.onnx.json