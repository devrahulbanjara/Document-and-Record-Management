# Document and Record Management System

## Introduction
The **Document and Record Management System (DRMS)** is designed to assist in verifying the authenticity of documents against a government database. This system is intended to help organizations detect fraudulent documents by checking if the provided document details match records stored in government portals. By facilitating a reliable way to cross-verify documents, the system aims to prevent fraud and enhance security in document handling.
## Goals
- **Automated Document Processing**: Utilize computer vision and OCR to automatically classify and extract data from uploaded government documents.
- **Fraud Detection**: Enable companies to verify the authenticity of documents by comparing them with records in a government database.
- **Ease of Use**: Provide a user-friendly interface for document submission and verification.
- **Accuracy**: Enhance the system's accuracy in detecting fraud through improved OCR and document classification.
- **Integration**: Seamlessly integrate with existing systems and databases used by organizations for document verification.

## Contributors
- **Rahul Dev Banjara**

## Project Architecture
1. **Frontend**: User interface for document upload and verification results.

2. **Backend**: Server-side processing, including OCR, document classification, and interaction with the government database.

3. **Document Processing Engine**: Storage for processed documents and verification records.

## Status

### Known Issues
- **OCR Accuracy on Low-Quality Scans**: The OCR models may have difficulty with documents that are poorly scanned or distorted.
- **Document Classification Confusion**: There may be issues with misclassifying documents that have similar formats but different types.
- **Scalability Limitations**: The system's performance may degrade with high volumes of simultaneous uploads or very high-resolution images.

### High-Level Next Steps
1. **Improve Data Quality**: Increase the quality and quantity of training data by incorporating a larger set of original and high-quality documents. This will enhance the accuracy and robustness of OCR and classification models.
2. **Develop Production-Grade Software**: Refactor the system to meet production-grade standards, including improving code quality, documentation, testing, and reliability. Implement best practices for software development to ensure robustness and maintainability.
3. **Integrate Relational Databases**: Replace the current dummy JSON database with a relational database system (e.g., PostgreSQL, MySQL) to better manage and query large volumes of data. This will improve data integrity, scalability, and performance.


# Usage
## Installation

### Prerequisites
- **Python 3.10** is required for this project. We recommend using a virtual environment to ensure compatibility.

### Virtual Environment Setup

1. Create a virtual environment:
    ```bash
    python3 -m venv venv
    ```

2. Activate the virtual environment:
    - On Linux/macOS:
        ```bash
        source venv/bin/activate
        ```
    - On Windows:
        ```bash
        venv\Scripts\activate
        ```

### Download Models
Before proceeding with installation, download the required models from the provided link. You will need the following models:
- **Classification Model**
- **License Model**
- **Passport Model**
- **Citizenship Model**

### Setting Up
1. Clone the repository:
    ```bash
    git clone https://github.com/devrahulbanjara/Document-and-Record-Management
    ```

2. Create a directory for the models:
    ```bash
    mkdir "trained models"
    ```

3. Place the downloaded model files into the `trained_models` directory.

4. Navigate to the project directory:
    ```bash
    cd Document-and-Record-Management
    ```

5. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

6. Run the application:
    ```bash
    streamlit run src/app.py
    ```

## Usage Instructions

# Data Source
- **Synthetic Datasets**: Text manually placed on template images to simulate real documents.
- **Lost and Found Groups**: Documents sourced from Facebook, Instagram, X, and similar platforms.
- **Government Samples**: Document samples provided by government sources for validation and comparison.

## Code Structure
- **Frontend**: User interface components for document upload and verification.
- **Backend**: Contains logic for processing documents, performing OCR, and interacting with the dummy JSON database.
- **Database Models**: Definitions and operations for interacting with JSON files used as a dummy database.

## Artifacts Location
Processed documents and verification results are stored in directories specified in the project configuration. The dummy database is maintained in JSON files within the project directory.

# Results
## Metrics 
The system is yet to be evaluated
## Evaluation Results
The system is yet to be evaluated
