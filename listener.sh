training_directory="training/sirus_salari"

while true; do
    file=$(inotifywait -e moved_to --format "%f" "$training_directory")
    if [[ "$file" == scan.jpg ]]; then
        python3 "facial_detection.py" "IMG_0378.MOV"
        break  # Exit the loop after processing one file
    fi
done
