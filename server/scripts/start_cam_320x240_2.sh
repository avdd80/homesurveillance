export LD_LIBRARY_PATH=/usr/src/mjpg-streamer/mjpg-streamer-experimental
/usr/src/mjpg-streamer/mjpg-streamer-experimental/mjpg_streamer -o "output_http.so -p 8080" -i "input_raspicam.so -x 320 -y 240 -fps 2"