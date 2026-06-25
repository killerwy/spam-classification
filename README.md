# spam-classification

> A desktop application for classifying emails as spam or legitimate (ham) using machine learning algorithms, built with Python and Tkinter.

[English](./README.md) | [中文](./README_zh.md)

![GitHub stars](https://img.shields.io/github/stars/killerwy/spam-classification?style=for-the-badge&logo=github) 
![GitHub forks](https://img.shields.io/github/forks/killerwy/spam-classification?style=for-the-badge&logo=github) 
![GitHub issues](https://img.shields.io/github/issues/killerwy/spam-classification?style=for-the-badge&logo=github) 
![Last commit](https://img.shields.io/github/last-commit/killerwy/spam-classification?style=for-the-badge&logo=github) 
![License](https://img.shields.io/badge/license-MIT-green?style=for-the-badge)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white) 

## 📑 Table of Contents

- [Description](#-description)
- [Features](#-features)
- [Tech Stack](#-tech-stack)
- [Quick Start](#-quick-start)
- [Usage Guide](#-usage-guide)
- [Project Structure](#-project-structure)
- [License](#-license)

## 📝 Description

A robust and user-friendly spam email classification system built with Python and machine learning algorithms. This application features a graphical user interface (GUI) that allows users to load email datasets, train multiple classification models, evaluate model performance, and classify individual emails as spam or legitimate (ham).

The system supports multiple machine learning algorithms and provides detailed performance metrics to help users understand model effectiveness, making it suitable for both educational purposes and practical spam detection tasks.

## ✨ Features

### Core Functionality
1. **Data Loading**: Load email datasets from directory structure (supports ham/spam subdirectories)
2. **Model Training**: 
   - Support for Naive Bayes, SVM, and Random Forest classifiers
   - Train-test split (80/20) for model evaluation
3. **Performance Evaluation**:
   - Detailed metrics (Accuracy, Precision, Recall, F1-Score)
   - Comprehensive classification reports
   - Clean, formatted display of evaluation results
4. **Email Classification**:
   - Predict spam/ham for manual email input
   - Import email content from text files
   - Probability scores for classification results

### User Interface
- Intuitive, organized GUI with labeled sections
- Scrolled text areas for email input and evaluation results
- Status bar for real-time operation feedback
- Custom fonts and styling for improved readability
- Error handling with user-friendly message boxes

## 🔧 Tech Stack

- Programming Languages: Python
- Libraries: scikit-learn, NumPy, Tkinter

## ⚡ Quick Start

1. Clone the repository

```bash

git clone https://github.com/killerwy/spam-classification.git
cd spam-classification

```

2. Create & activate a virtual environment

```bash

# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python -m venv venv && source venv/bin/activate

```

3. Install required dependencies

```bash

pip install -r requirements.txt

```

4. Run the application

```bash

python main.py

```

## 📖 Usage Guide

### 1. Loading Data
- Click "Browse..." to select the root directory of your email dataset

  > Recommended dataset: Enron Email Dataset. Official source page (CMU): https://www.cs.cmu.edu/~enron/; AUEB labeled Enron-Spam subset: https://www2.aueb.gr/users/ion/data/enron-spam/

- The dataset should follow this structure:
  ```
  dataset/
  ├── [folder1]/
  │   ├── ham/      # Legitimate emails (label 0)
  │   └── spam/     # Spam emails (label 1)
  ├── [folder2]/    # Additional subdirectories (optional)
  │   ├── ham/
  │   └── spam/
  ├── ...
  └── [foldern]/    # Additional subdirectories (optional)
      ├── ham/
      └── spam/
  ```
- Click "Load Data" to process the dataset (shows email count statistics)

### 2. Training Models
- Select a classifier from the dropdown menu (Naive Bayes default)
- Click "Train Model" to train all available models
- View detailed performance metrics in the evaluation results area

### 3. Classifying Emails
- Paste email content into the "Email Classification" text area (or import from file)
- Click "Predict" to classify the email
- View results (spam/ham) and probability scores
- Use "Clear" to reset the input area

## 📁 Project Structure

```
spam-classification/
├── main.py                # Application entry point
├── interface.py           # GUI implementation (Tkinter)
├── model.py               # Machine learning model logic
├── requirements.txt       # Project dependencies
├── README.md              # English project introduction, usage, deployment guide
├── README_zh.md           # Chinese version of project documentation
├── LICENSE                # Open source license file
└── .gitignore             # Git ignore configuration file
```

## 📜 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

---
*This README was generated with ❤️ by [ReadmeBuddy](https://readmebuddy.com)*
