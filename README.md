# self.checkout

This project is a self-checkout system designed to streamline the shopping experience.

More specifically, the end-goal is to have a program that will allow for in-store shoppers to puruchase
alcoholic beverages from the self-checkout registers.

Currently, you're only allowed to purchase alcoholic beverages at employee-operated registers.

The process usually goes as follows:

- Employee scans the alcoholic beverage barcode
- Emplyee scans customer's ID to verify it's a legitimate ID
- Employee looks at the ID photo and matches the photo to the customer

This project aims to have AI handle step 3, so that the customer can handle steps 1 and 2 if they wish to do so.

More specifically, this will be accomplished by having the ML model train on just 1 original image (the ID photo).

The intent is that this original photo will be aquired through hardware such as a photo scanner.

Next, the program will generate new augmented images so that the model has more images to train with.

Finally, the program will validate the customer by taking 5 frames from video footage at the self-checkout station 
as validation images.

## Installation

Clone the repository to your local machine:

```bash
git clone https://github.com/sirus-the-beaver/self.checkout.git
```
Navigate to the project directory, activate virtual environment, and install the required dependencies:

```bash
cd self.checkout
python -m venv venv
source venv/bin/activate
python -m pip install -r requirements.txt
```

## Usage

Run from the terminal:
```bash
python facial_detection.py /path/to/video
```

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License
MIT

