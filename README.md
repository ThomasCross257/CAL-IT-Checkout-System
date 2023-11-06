# CAL-IT-Checkout-System
Laptop checkout system for the CSUSB College of Arts and Letters

<hr/>

## Debug locally
<p>Make a dotenv file with a postgres DB URI</p>

```
DATABASE_URI = "postgresql://username:password@location/laptop-checkout"
```
Initialize the virtual environment
```
python -m venv ./venv
cd venv\scripts
activate
pip install -r requirements.txt
```

Run the app by typing

```
flask run main.py
```
