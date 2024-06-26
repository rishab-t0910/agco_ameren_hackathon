# occuPi - University of Illinois Research Park Hackathon 2024

Occupi - near real-time and forecasted room occupancy using edge computing and zero-shot transfer learning.

## Team Name: Agco x Ameren

### Members

Samuel Gerstein, Caleb Larson, Angie Lewis, Atharva Naik, Rishab Tirupathi

### Problem

We often see people in libraries at UofI counting the number of people in the library via a clicker. The all-to-familiar clicking noise passing the hall every hour is well known across students. This utilises a lot of manpower and manual labour, which could be used for other more productive activities. Additionally, during times of high traffic to the library (before breaks and around finals), it is hard to know whether there is avaiable seating now, or in the future.

### Proposed Solution

The solution is to combine sensors and predictive modeling to showcase what the current seating capacity is, and what the future is likely to be. This enables students to better plan when to reach the library, and whether or not it is worth their time.

### Future Work

We hope to also implement a recommendation system that provides recommendations for nearby libraries with sufficient capacity.

## System Architecture

![UML](/assets/uml.png)

## Repository setup

We recommend creating a [python virtual environment](https://docs.python.org/3/tutorial/venv.html) to silo dependencies for the project.

```
pip install -r requirements.txt
```

You will also need a Google Cloud JSON key (specifically for Firestore) that you
can store in a `.env` file structured as follows:

```
CREDENTIALS_JSON=<path_to_credentials>
```
