training_directory="/training"

while true; do
    file=$(inotifywait -e create --format "%f" "$training_directory")
    if [[ "$file" == *.jpg ]]; then
        python3 "facial_detection.py"
        break  # Exit the loop after processing one file
    fi
done
