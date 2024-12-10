# PopCornCritic

Inspired by SensCritique, PopCornCritic is an API that enables users to search, rate, and review movies while interacting with other users through personalized recommendations.

Users can follow **scouts**, trusted individuals who recommend movies based on their own opinions. They can explore ratings and reviews from other users and access curated movie lists by the scouts they follow. Active users have the opportunity to become scouts themselves.

This application is built with **FastAPI**, designed for programmatic use rather than direct user interaction. In the future, one possible improvement could be the addition of a user-friendly interface, making it easier for people to interact directly with the app.

---

## Table of Contents
1. [Introduction](#introduction)  
2. [Prerequisites](#prerequisites)  
3. [How to Run the App](#how-to-run-the-app)  
4. [Features Overview](#features-overview)  

---

## Introduction

Welcome to PopCornCritic! This project was created as part of an academic exercise by a group of second-year students at the ENSAI engineering school in Bruz, France. The goal of this application is to provide a dynamic platform for movie enthusiasts, allowing them to share their opinions, discover new films, and interact with a community of like-minded users.

This README will guide you through the setup, execution, and core features of the API.

---

## Prerequisites

To ensure everything runs smoothly, make sure your environment meets the following requirements:

### Python Version Required
```bash
python --version  
Python 3.9 or later  

Required Libraries
Install the necessary dependencies using pip or conda:

pyJWT
For pip
pip install --upgrade pyJWT

For conda
conda install -c conda-forge pyjwt

How to Run the App
Once all dependencies are installed, you can run the application by opening a terminal and entering the following command:

bash
python __main__.py
The application will start and expose the API endpoints for interaction. Use tools such as Postman or curl to test the API.


