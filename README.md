# self.checkout

This project is a self-checkout system designed to streamline the shopping experience.

The end-goal is to have a program that will allow for in-store shoppers to puruchase
alcoholic beverages from the self-checkout registers.

Currently, you're only allowed to purchase alcoholic beverages at employee-operated registers.

The process usually goes as follows:

- Employee scans the alcoholic beverage barcode
- Emplyee scans customer's ID to verify it's a legitimate ID
- Employee looks at the ID photo and matches the photo to the customer

This project aims to have AI handle step 3, so that the customer can handle steps 1 and 2 if they wish to do so at the self checkout register.

This will be accomplished by having the ML model train on just 1 original image (the ID photo).

The process goes as follows:

- Customer scans the alcoholic beverage barcode
- Customer scans their ID's barcode so the computer verifies it's legitimate
- Customer holds their ID up to a camera
- This program will capture a picture of their ID as well as a short video clip of the customer
- The program will then send the ID image down an image augmentation pipeline to generate an artificially larger training dataset
- Next, the program will train on the original ID image and the augmented images using a CNN model (currently using HOG model, but CNN will be used in practice)
- Then, the program will try to validate the customer by testing image frames from the video recorded of the customer earlier
- If the model determines that the face in the video frames is the same as the ID image, then the customer is fully verified as able to purchase the alcohol and they can continue scanning items

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

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License
MIT

