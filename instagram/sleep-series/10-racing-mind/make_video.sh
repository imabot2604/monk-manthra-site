#!/bin/bash
# 5 square slides -> one 1080x1920 reel, slow crossfades, calm bed under it.
# Text is never scaled or zoomed (it would soften) — the only motion is the dissolve.
set -e
BG="#F4F1EC"; D=6.0; X=0.7   # per-slide seconds, crossfade seconds
IN=(); FILTER=""
i=0
for f in jpg/slide-*.jpg; do
  IN+=(-loop 1 -t $D -i "$f")
  FILTER+="[$i:v]scale=1080:1080,pad=1080:1920:0:420:color=$BG,format=yuv420p,fps=30,setsar=1[v$i];"
  i=$((i+1))
done
# chain the dissolves
FILTER+="[v0][v1]xfade=transition=fade:duration=$X:offset=$(echo "$D-$X"|bc)[x1];"
FILTER+="[x1][v2]xfade=transition=fade:duration=$X:offset=$(echo "2*$D-2*$X"|bc)[x2];"
FILTER+="[x2][v3]xfade=transition=fade:duration=$X:offset=$(echo "3*$D-3*$X"|bc)[x3];"
FILTER+="[x3][v4]xfade=transition=fade:duration=$X:offset=$(echo "4*$D-4*$X"|bc)[vout]"

ffmpeg -y -loglevel error "${IN[@]}" -i audio/calm-bed.wav \
  -filter_complex "$FILTER" \
  -map "[vout]" -map 5:a \
  -c:v libx264 -preset slow -crf 18 -pix_fmt yuv420p -r 30 \
  -c:a aac -b:a 192k -ar 44100 -shortest \
  -movflags +faststart video/racing-mind.mp4
ffprobe -v error -show_entries format=duration,size -show_entries stream=codec_name,width,height,r_frame_rate -of default=nw=1 video/racing-mind.mp4
