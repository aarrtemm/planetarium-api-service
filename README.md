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

## DB 
![image](https://github.com/aarrtemm/planetarium-api-service/assets/115632117/c256677a-2a41-4e35-ae3b-8721b3db187b)

### Main page
![image](https://github.com/aarrtemm/planetarium-api-service/assets/115632117/b505b741-e6a5-4694-bfb0-175410b4e9eb)

### Register page
![image](https://github.com/aarrtemm/planetarium-api-service/assets/115632117/0787953c-a268-4350-856f-97f2a0f50dcd)

### Get token page
![image](https://github.com/aarrtemm/planetarium-api-service/assets/115632117/3dbb8283-4a65-41e3-b900-d827b7d2d741)

### Refresh token page
![image](https://github.com/aarrtemm/planetarium-api-service/assets/115632117/56335a0e-83b9-4254-833e-9ab938d3ab25)

### Verify token page
![image](https://github.com/aarrtemm/planetarium-api-service/assets/115632117/7c444fa5-7598-46be-9da1-e424da9cc76d)

### Profile page
![image](https://github.com/aarrtemm/planetarium-api-service/assets/115632117/f2a21a6c-2361-43d2-9c19-d75ff49fea2f)

### API root page
![image](https://github.com/aarrtemm/planetarium-api-service/assets/115632117/4e0deda4-a794-49aa-b107-ba087ec9f031)

### Themes page
![image](https://github.com/aarrtemm/planetarium-api-service/assets/115632117/1ca6e34f-f018-4e41-b282-bde16abaa565)

### Astronomy shows list page
![image](https://github.com/aarrtemm/planetarium-api-service/assets/115632117/25c0ac5f-c2b0-4f06-a906-13badb43337d)

### Astronomy shows detail page
![image](https://github.com/aarrtemm/planetarium-api-service/assets/115632117/90940e50-7a2d-449d-ab51-bad57746943e)

### Astronomy page upload image page
- This page allows only admins to upload images for the astronomy show.
![image](https://github.com/aarrtemm/planetarium-api-service/assets/115632117/c7b82c5c-2cb9-4138-8d95-efdee2575ced)

### Domes page 
![image](https://github.com/aarrtemm/planetarium-api-service/assets/115632117/e3ae0472-64ee-438b-9737-f33861e48351)

### Show sessions list page 
![image](https://github.com/aarrtemm/planetarium-api-service/assets/115632117/9f683e45-5eb7-4004-88b9-497ae4362585)

### Show sessions detail page
![image](https://github.com/aarrtemm/planetarium-api-service/assets/115632117/dfb622ef-6cd5-44aa-93a8-e417257b5e3c)

### Reservations list page
![image](https://github.com/aarrtemm/planetarium-api-service/assets/115632117/f7dce340-3641-4926-8d96-37330f565b38)








