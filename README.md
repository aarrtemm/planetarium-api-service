# Planetarium API Service
This is a web application for an online to book ticket in Planetarium. The project aims to provide a user-friendly and visually attractive platform for guests to browse and reserve tickets.
## Features
- Browse the shows: Users can explore various themes of astronomy shows, filter shows based on different parameters, and view detailed information about each item.
- Book a ticket: Users can book at Astronomy show.
- Reservation process: Users can proceed to the reservation page, provide necessary information such as name is astronomy show and date, places, domes and complete the order.
- User authentication: Users can create accounts, log in with help token, and manage their profiles.
## Technologies Used
- Python with Django, Django REST framework for the backend
- SQLite3 and PostgreSQL for the database

## Check it out!

[Planetarium API Service project deployed to Render](https://planetarium-api-service.onrender.com)

## Installation

1.Clone the repository:
```bush
git clone https://github.com/your_name/planetarium-api-service.git
```

2.Install the dependencies:
```bush
pip install -r requirements.txt
```
3.Set up the database:
- Run the migrations
```bush
python manage.py migrate
```

4.Start the development server:
```bash
python manage.py runserver
```

5.First step is register http://localhost:8000/api/user/register

6.Second step is get auth token http://localhost:8000/api/user/token



## Contributing
Contributions are welcome! If you have any suggestions, bug reports, or feature requests, please open an issue or submit a pull request.
