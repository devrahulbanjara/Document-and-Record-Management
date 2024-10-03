# Document and Record Management System

## Introduction
<div align="center">

![Animate](docs/animate.gif)

</div>
The Document and Record Management System (DRMS) is designed to assist in verifying the authenticity of documents against a government database. This system is intended to help organizations detect fraudulent documents by checking if the provided document details match records stored in government portals. By facilitating a reliable way to cross-verify documents, the system aims to prevent fraud and enhance security in document handling.

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
1. **Multi-Language Support**: Implement support for multiple languages in the OCR and text extraction processes to accommodate diverse user needs and enhance usability across different regions.
2. **Custom OCR Fine-Tuning**: Fine-tune the OCR model with custom datasets for improved accuracy on specific document types.
3. **Improve Data Quality**: Increase the quality and quantity of training data by incorporating a larger set of original and high-quality documents. This will enhance the accuracy and robustness of OCR and classification models.
4. **Develop Production-Grade Software**: Refactor the system to meet production-grade standards, including improving code quality, documentation, testing, and reliability. Implement best practices for software development to ensure robustness and maintainability.
5. **Integrate Relational Databases**: Replace the current dummy JSON database with a relational database system (e.g., PostgreSQL, MySQL) to better manage and query large volumes of data. This will improve data integrity, scalability, and performance.

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

# Data Source
- **Synthetic Datasets**: Text manually placed on template images to simulate real documents.
- **Lost and Found Groups**: Documents sourced from Facebook, Instagram, X, and similar platforms.
- **Government Samples**: Document samples provided by government sources for validation and comparison.

## Code Structure

### Frontend

- **Path**: `src/app.py`
- **Description**: Provides the user interface for document upload, classification, and verification using Streamlit. Users can upload documents via webcam or file, which are then classified and verified.

### Backend

#### Classification
- **Path**: `src/classification.py`
- **Description**: Classifies documents into categories such as citizenship, license, passport, and others.

#### Detection
- **Path**: `src/detection.py`
- **Description**: Detects regions of interest (e.g., name, date of birth) in classified documents using YOLOv8 models.

#### OCR
- **Path**: `src/ocrtext.py`
- **Description**: Extracts text from detected regions using Optical Character Recognition (OCR).

#### Filtering
- **Paths**:
  - `src/filter_citizenship.py`
  - `src/filter_license.py`
  - `src/filter_passport.py`
- **Description**: Filters the text extracted via OCR to retrieve relevant details like name, citizenship number, etc., for different document types (citizenship, license, passport).

#### Image Preprocessing
- **Path**: `src/process_image.py`
- **Description**: Performs image preprocessing tasks, including resizing, orientation correction, and binarization, before classification and detection.

#### Validation
- **Paths**:
  - `src/validate_citizenship.py`
  - `src/validate_document.py`
- **Description**: Validates the extracted data against records stored in the database to ensure document authenticity.

#### Plotting
- **Path**: `src/plot_details.py`
- **Description**: Generates visual plots and results for detected regions and classified data.

### Database Models

- **Path**: `src/database.py`
- **Description**: Defines operations to interact with the `database.json` file, which acts as a dummy database for storing and verifying document details.

### Notebooks

- **Path**: `notebooks/`
- **Description**: Contains Jupyter notebooks for model experimentation, including:
  - Classification model training and inference (`notebooks/Classification/`)
  - YOLOv8 model training and inference (`notebooks/YOLOv8/`)
  - OCR experiments using EasyOCR (`notebooks/OCR/`)
  - Text filtering experiments after OCR output (`notebooks/Text Filtering/`)

### Tests

- **Path**: `tests/test_template.py`
- **Description**: Unit tests to ensure the correctness of various components in the document verification system.

# Results

## Classification Model Evaluation
- **Model Accuracy**: 0.98

| Metric    | Citizenship | License | Passport | Others | Weighted Average |
|-----------|-------------|---------|----------|--------|------------------|
| Precision | 0.98        | 0.95    | 1.00     | 0.98   | 0.98             |
| Recall    | 0.98        | 0.98    | 0.96     | 0.98   | 0.98             |
| F1 Score  | 0.98        | 0.96    | 0.98     | 0.98   | 0.98             |

## YOLOv8 Models Evaluation

### Citizenship Model
| Metric    | Citizenship No. | District | Gender | Name  | Year  | Overall |
|-----------|-----------------|----------|--------|-------|-------|---------|
| Precision | 0.949           | 0.931    | 0.956  | 0.971 | 0.944 | 0.949   |
| Recall    | 0.941           | 0.965    | 0.968  | 1.000 | 0.872 | 0.941   |
| mAP@50    | 0.970           | 0.978    | 0.974  | 0.995 | 0.951 | 0.970   |
| mAP@50-95 | 0.577           | 0.622    | 0.556  | 0.555 | 0.610 | 0.577   |

### License Model
| Metric    | Citizenship No. | Contact No. | DOB    | License No. | Name  | Overall |
|-----------|-----------------|-------------|--------|-------------|-------|---------|
| Precision | 0.798           | 0.615       | 0.773  | 0.905       | 0.955 | 0.809   |
| Recall    | 0.923           | 0.917       | 0.910  | 0.947       | 0.954 | 0.930   |
| mAP@50    | 0.892           | 0.892       | 0.888  | 0.949       | 0.945 | 0.913   |
| mAP@50-95 | 0.506           | 0.546       | 0.551  | 0.573       | 0.448 | 0.533   |

### Passport Model
| Metric    | Citizenship No. | DOB    | Name  | Passport No. | Surname | Overall |
|-----------|-----------------|--------|-------|--------------|---------|---------|
| Precision | 0.994           | 0.982  | 0.982 | 0.938        | 0.992   | 0.978   |
| Recall    | 0.978           | 0.977  | 0.989 | 0.979        | 0.989   | 0.983   |
| mAP@50    | 0.979           | 0.986  | 0.994 | 0.989        | 0.995   | 0.989   |
| mAP@50-95 | 0.738           | 0.778  | 0.772 | 0.669        | 0.760   | 0.743   |

## Overall System Evaluation

| Metric    | Genuine | Fraudulent |
|-----------|---------|------------|
| Precision | 1.0     | 0.6        |
| Recall    | 0.7647  | 1.0        |
| F1 Score  | 0.8667  | 0.75       |

- **Overall Accuracy**: 82.61%
