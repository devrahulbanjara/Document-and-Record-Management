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
To begin this project, use the included `Makefile`

#### Creating Virtual Environment

This package is built using `python-3.10`. 
We recommend creating a virtual environment and using a matching version to ensure compatibility.

#### pre-commit

`pre-commit` will automatically format and lint your code. You can install using this by using
`make use-pre-commit`. It will take effect on your next `git commit`

#### pip-tools

The method of managing dependencies in this package is using `pip-tools`. To begin, run `make use-pip-tools` to install. 

Then when adding a new package requirement, update the `requirements.in` file with 
the package name. You can include a specific version if desired but it is not necessary. 

To install and use the new dependency you can run `make deps-install` or equivalently `make`

If you have other packages installed in the environment that are no longer needed, you can you `make deps-sync` to ensure that your current development environment matches the `requirements` files. 

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
