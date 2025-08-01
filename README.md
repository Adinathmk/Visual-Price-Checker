# Visual Price Comparison Web Application

This Flask web application allows users to compare prices of products detected in images using the Google Cloud Vision API. Users can upload an image, and the application will extract URLs related to e-commerce sites and their corresponding prices.

#### it's still under development and not completely working on deployed server due to some issues.But it Works Properly on local host So try It

## Features

- **Image Upload:** Users can upload an image containing products they want to compare prices for.
- **Google Cloud Vision Integration:** Utilizes the Google Cloud Vision API to detect web entities in the uploaded image.
- **Price Scraping:** Scrapes prices from various e-commerce websites corresponding to the detected products.
- **Comparison Display:** Presents a comparison of prices for the detected products on the web page.

## How It Works

1. **Image Upload:** Users upload an image through the web interface.
2. **Web Entity Detection:** The application processes the uploaded image using the Google Cloud Vision API to detect web entities.
3. **Price Extraction:** Extracted URLs related to e-commerce sites are matched with predefined XPath expressions to scrape prices.
4. **Comparison Display:** The comparison results, including product URLs and prices, are displayed on the web page for users to view.

## Performance

- **Scalability:** The application is designed to handle multiple concurrent requests and can scale with demand.
- **Processing Time:** The processing time varies depending on the size of the uploaded image and the number of detected web entities. However, efforts have been made to optimize performance where possible.
- **Reliability:** The application aims to provide reliable price comparison results by utilizing established web scraping techniques and the Google Cloud Vision API.

## Installation and Usage

Please refer to the following sections for instructions on how to install and use the application.

### Installation

1. **Clone the repository:**

    ```bash
    git clone https://github.com/your-username/your-repository.git
    cd your-repository
    ```

2. **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

3. **Set up environment variables:**

    - Create a `.env` file in the root directory.
    - Define the following environment variables:

        ```plaintext
        FLASK_SECRET_KEY=your_secret_key
        CHROME_BINARY_LOCATION=/path/to/chrome/binary
        CHROME_DRIVER_PATH=/path/to/chromedriver
        GOOGLE_APPLICATION_CREDENTIALS=/path/to/google_credentials.json
        UPLOAD_FOLDER=uploads
        ```

4. **Run the application:**

    ```bash
    python app.py
    ```

5. **Access the application:**

    Open your web browser and go to `http://localhost:5000`.


## Contributing

Contributions are welcome! If you'd like to contribute to this project, please follow the steps outlined below.

### How to Contribute

1. Fork the repository.
2. Create a new branch (`git checkout -b feature/new-feature`).
3. Make your changes and commit them (`git commit -am 'Add new feature'`).
4. Push your changes to the branch (`git push origin feature/new-feature`).
5. Create a new Pull Request.

## Acknowledgements

This project relies on the following technologies and libraries:

- [Flask](https://flask.palletsprojects.com/): Web framework for Python.
- [Google Cloud Vision API](https://cloud.google.com/vision): For web entity detection.
- [Selenium](https://www.selenium.dev/): For web scraping.
- [Beautiful Soup](https://www.crummy.com/software/BeautifulSoup/): For HTML parsing.
- [Bootstrap](https://getbootstrap.com/): For front-end design.

## Contact

For any questions or inquiries, please contact [adinathmkclt@gmail.com](mailto:adinathmkclt@gmail.com).
